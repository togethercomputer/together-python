from __future__ import annotations

import os
import requests
import shutil
import stat
import tempfile
import uuid
from functools import partial
from pathlib import Path
from typing import Tuple
from tqdm.utils import CallbackIOWrapper

from filelock import FileLock
from requests.structures import CaseInsensitiveDict
from tqdm import tqdm

import together.utils
from together.abstract import api_requestor

from together.constants import DISABLE_TQDM, DOWNLOAD_BLOCK_SIZE, MAX_RETRIES

from together.error import (
    DownloadError,
    FileTypeError,
    APIError,
    AuthenticationError,
)
from together.types import TogetherClient, TogetherRequest, FileResponse, FilePurpose
from together.together_response import TogetherResponse


def chmod_and_replace(src: Path, dst: Path) -> None:
    """Set correct permission before moving a blob from tmp directory to cache dir.

    Do not take into account the `umask` from the process as there is no convenient way
    to get it that is thread-safe.
    """

    # Get umask by creating a temporary file in the cache folder.
    tmp_file = dst.parent.parent / f"tmp_{uuid.uuid4()}"

    try:
        tmp_file.touch()

        cache_dir_mode = Path(tmp_file).stat().st_mode

        os.chmod(src, stat.S_IMODE(cache_dir_mode))

    finally:
        tmp_file.unlink()

    shutil.move(src, dst)


def _get_file_size(
    headers: CaseInsensitiveDict[str],
) -> int:
    """
    Extracts file size from header
    """
    total_size_in_bytes = 0

    parts = headers.get("Content-Range", "").split(" ")

    if len(parts) == 2:
        range_parts = parts[1].split("/")

        if len(range_parts) == 2:
            total_size_in_bytes = int(range_parts[1])

    assert total_size_in_bytes != 0, "Unable to retrieve remote file."

    return total_size_in_bytes


def _prepare_output(
    headers: CaseInsensitiveDict[str],
    step: int = -1,
    output: Path | None = None,
    remote_name: str | None = None,
) -> Path:
    """
    Generates output file name from remote name and headers
    """
    if output:
        return output

    content_type = str(headers.get("content-type"))

    assert remote_name, (
        "No model name found in fine_tune object. "
        "Please specify an `output` file name."
    )

    if step > 0:
        remote_name += f"-checkpoint-{step}"

    if "x-tar" in content_type.lower():
        remote_name += ".tar.gz"

    elif "zstd" in content_type.lower() or step != -1:
        remote_name += ".tar.zst"

    else:
        raise FileTypeError(
            f"Unknown file type {content_type} found. Aborting download."
        )

    return Path(remote_name)


class DownloadManager:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def get_file_metadata(
        self,
        url: str,
        output: Path | None = None,
        remote_name: str | None = None,
        fetch_metadata: bool = False,
    ) -> Tuple[Path, int]:
        """
        gets remote file head and parses out file name and file size
        """

        if not fetch_metadata:
            if isinstance(output, Path):
                file_path = output
            else:
                assert isinstance(remote_name, str)
                file_path = Path(remote_name)

            return file_path, 0

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response = requestor.request_raw(
            options=TogetherRequest(
                method="GET",
                url=url,
                headers={"Range": "bytes=0-1"},
            ),
            remaining_retries=MAX_RETRIES,
            stream=False,
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise APIError(
                "Error fetching file metadata", http_status=response.status_code
            ) from e

        headers = response.headers

        assert isinstance(headers, CaseInsensitiveDict)

        file_path = _prepare_output(
            headers=headers,
            output=output,
            remote_name=remote_name,
        )

        file_size = _get_file_size(headers)

        return file_path, file_size

    def download(
        self,
        url: str,
        output: Path | None = None,
        remote_name: str | None = None,
        fetch_metadata: bool = False,
    ) -> Tuple[str, int]:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # pre-fetch remote file name and file size
        file_path, file_size = self.get_file_metadata(
            url, output, remote_name, fetch_metadata
        )

        temp_file_manager = partial(
            tempfile.NamedTemporaryFile, mode="wb", dir=file_path.parent, delete=False
        )

        # Prevent parallel downloads of the same file with a lock.
        lock_path = Path(file_path.as_posix() + ".lock")

        with FileLock(lock_path):
            with temp_file_manager() as temp_file:
                response = requestor.request_raw(
                    options=TogetherRequest(
                        method="GET",
                        url=url,
                    ),
                    remaining_retries=MAX_RETRIES,
                    stream=True,
                )

                try:
                    response.raise_for_status()
                except Exception as e:
                    os.remove(lock_path)
                    raise APIError(
                        "Error downloading file", http_status=response.status_code
                    ) from e

                if not fetch_metadata:
                    file_size = int(response.headers.get("content-length", 0))

                assert file_size != 0, "Unable to retrieve remote file."

                with tqdm(
                    total=file_size,
                    unit="B",
                    unit_scale=True,
                    desc=f"Downloading file {file_path.name}",
                    disable=bool(DISABLE_TQDM),
                ) as pbar:
                    for chunk in response.iter_content(DOWNLOAD_BLOCK_SIZE):
                        pbar.update(len(chunk))
                        temp_file.write(chunk)

            # Raise exception if remote file size does not match downloaded file size
            if os.stat(temp_file.name).st_size != file_size:
                DownloadError(
                    f"Downloaded file size `{pbar.n}` bytes does not match "
                    f"remote file size `{file_size}` bytes."
                )

            # Moves temp file to output file path
            chmod_and_replace(Path(temp_file.name), file_path)

        os.remove(lock_path)

        return file_path.as_posix(), file_size


class UploadManager:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    @classmethod
    def _redirect_error_handler(
        cls, requestor: api_requestor.APIRequestor, response: requests.Response
    ) -> None:
        if response.status_code == 401:
            raise AuthenticationError(
                "This job would exceed your free trial credits. "
                "Please upgrade to a paid account through "
                "Settings -> Billing on api.together.ai to continue.",
            )
        elif response.status_code != 302:
            raise APIError(
                f"Unexpected error raised by endpoint: {response.content.decode()}, headers: {response.headers}",
                http_status=response.status_code,
            )

    def redirect_policy(
        self, url: str, file: Path, purpose: FilePurpose
    ) -> Tuple[str, str]:
        data = {
            "purpose": purpose.value,
            "file_name": file.name,
        }

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        method = "POST"

        headers = together.utils.get_headers(method, requestor.api_key)

        response = requestor.request_raw(
            options=TogetherRequest(
                method=method,
                url=url,
                params=data,
                allow_redirects=False,
                override_headers=True,
                headers=headers,
            ),
            remaining_retries=MAX_RETRIES,
        )

        self._redirect_error_handler(requestor, response)

        redirect_url = response.headers["Location"]
        file_id = response.headers["X-Together-File-Id"]

        return redirect_url, file_id

    def callback(self, url: str) -> TogetherResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url=url,
            ),
        )

        return response

    def upload(
        self,
        url: str,
        file: Path,
        purpose: FilePurpose,
        redirect: bool = False,
    ) -> FileResponse:
        file_id = None

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        redirect_url = None
        if redirect:
            redirect_url, file_id = self.redirect_policy(url, file, purpose)

        file_size = os.stat(file.as_posix()).st_size

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            desc=f"Uploading file {file.name}",
            disable=bool(DISABLE_TQDM),
        ) as pbar:
            with file.open("rb") as f:
                wrapped_file = CallbackIOWrapper(pbar.update, f, "read")

                if redirect:
                    callback_response = requestor.request_raw(
                        options=TogetherRequest(
                            method="PUT",
                            url=redirect_url,
                            params=wrapped_file,
                            override_headers=True,
                        ),
                        absolute=True,
                        remaining_retries=MAX_RETRIES,
                    )
                else:
                    response, _, _ = requestor.request(
                        options=TogetherRequest(
                            method="PUT",
                            url=url,
                            params=wrapped_file,
                        ),
                    )

        if redirect:
            assert isinstance(callback_response, requests.Response)

            if not callback_response.status_code == 200:
                raise APIError(
                    f"Error code: {callback_response.status_code} - Failed to process uploaded file"
                )

            response = self.callback(f"{url}/{file_id}/preprocess")

        assert isinstance(response, TogetherResponse)

        return FileResponse(**response.data)
