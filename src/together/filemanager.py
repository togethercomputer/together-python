from __future__ import annotations

import os
import shutil
import stat
import tempfile
import uuid
from functools import partial
from pathlib import Path
from typing import Tuple

from filelock import FileLock
from requests.structures import CaseInsensitiveDict
from tqdm import tqdm

from together.abstract import api_requestor

from together.constants import (
    DISABLE_TQDM,
    DOWNLOAD_BLOCK_SIZE,
)

from together.error import DownloadError, FileTypeError
from together.types import TogetherClient, TogetherRequest


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


class DownloadManager:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    def _get_file_size(
        self,
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
        self,
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

    def get_file_metadata(
        self, url: str, output: Path | None = None, remote_name: str | None = None
    ) -> Tuple[Path, int]:
        """
        gets remote file head and parses out file name and file size
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="GET", url=url, headers={"Range": "bytes=0-1"}, return_raw=True
            ),
            stream=False,
            return_raw=True,
        )

        headers = response.headers

        assert isinstance(headers, CaseInsensitiveDict)

        file_path = self._prepare_output(
            headers=headers,
            output=output,
            remote_name=remote_name,
        )

        file_size = self._get_file_size(headers)

        return file_path, file_size

    def download(
        self,
        url: str,
        output: Path | None = None,
        remote_name: str | None = None,
        fetch_metadata: bool = False,
    ) -> Tuple[Path, int]:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # pre-fetch remote file name and file size
        if fetch_metadata:
            file_path, file_size = self.get_file_metadata(url, output, remote_name)
        else:
            if isinstance(output, Path):
                file_path = output
            else:
                assert isinstance(remote_name, str)
                file_path = Path(remote_name)

        temp_file_manager = partial(
            tempfile.NamedTemporaryFile, mode="wb", dir=file_path.parent, delete=False
        )

        # Prevent parallel downloads of the same file with a lock.
        lock_path = Path(file_path.name + ".lock")

        lock = FileLock(lock_path)

        lock.acquire()

        with temp_file_manager() as temp_file:
            response, _, _ = requestor.request(
                options=TogetherRequest(
                    method="GET",
                    url=url,
                ),
                stream=True,
                return_raw=True,
            )

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

        lock.release()

        os.remove(lock_path)

        return file_path, file_size


class UploadManager:
    def __init__(self) -> None:
        pass

    def upload(self) -> None:
        raise NotImplementedError()
