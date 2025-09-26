from __future__ import annotations

import math
import os
import shutil
import stat
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from filelock import FileLock
from requests.structures import CaseInsensitiveDict
from tqdm import tqdm

from together.abstract import api_requestor
from together.constants import (
    DISABLE_TQDM,
    DOWNLOAD_BLOCK_SIZE,
    MAX_CONCURRENT_PARTS,
    MAX_FILE_SIZE_GB,
    MAX_RETRIES,
    MIN_PART_SIZE_MB,
    NUM_BYTES_IN_GB,
    TARGET_PART_SIZE_MB,
    MAX_MULTIPART_PARTS,
    MULTIPART_UPLOAD_TIMEOUT,
)
from together.error import (
    APIError,
    AuthenticationError,
    DownloadError,
    FileTypeError,
    ResponseError,
)
from together.together_response import TogetherResponse
from together.types import (
    FilePurpose,
    FileResponse,
    FileType,
    TogetherClient,
    TogetherRequest,
)
from tqdm.utils import CallbackIOWrapper
import together.utils


def chmod_and_replace(src: Path, dst: Path) -> None:
    """Set correct permission before moving a blob from tmp directory to cache dir.

    Do not take into account the `umask` from the process as there is no convenient way
    to get it that is thread-safe.
    """

    # Get umask by creating a temporary file in the cache folder.
    tmp_file = dst.parent / f"tmp_{uuid.uuid4()}"

    try:
        tmp_file.touch()

        cache_dir_mode = Path(tmp_file).stat().st_mode

        os.chmod(src.as_posix(), stat.S_IMODE(cache_dir_mode))

    finally:
        tmp_file.unlink()

    shutil.move(src.as_posix(), dst.as_posix())


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

    else:
        remote_name += ".tar.zst"

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

        with FileLock(lock_path.as_posix()):
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

        return str(file_path.resolve()), file_size


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

    def get_upload_url(
        self,
        url: str,
        file: Path,
        purpose: FilePurpose,
        filetype: FileType,
    ) -> Tuple[str, str]:
        data = {
            "purpose": purpose.value,
            "file_name": file.name,
            "file_type": filetype.value,
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
            if file.suffix == ".jsonl":
                filetype = FileType.jsonl
            elif file.suffix == ".parquet":
                filetype = FileType.parquet
            elif file.suffix == ".csv":
                filetype = FileType.csv
            else:
                raise FileTypeError(
                    f"Unknown extension of file {file}. "
                    "Only files with extensions .jsonl and .parquet are supported."
                )
            redirect_url, file_id = self.get_upload_url(url, file, purpose, filetype)

        file_size = os.stat(file).st_size

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
                    f"Error during file upload: {callback_response.content.decode()}, headers: {callback_response.headers}",
                    http_status=callback_response.status_code,
                )

            response = self.callback(f"{url}/{file_id}/preprocess")

        assert isinstance(response, TogetherResponse)

        return FileResponse(**response.data)


class MultipartUploadManager:
    """Handles multipart uploads for large files"""

    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.max_concurrent_parts = MAX_CONCURRENT_PARTS

    def upload(
        self,
        url: str,
        file: Path,
        purpose: FilePurpose,
    ) -> FileResponse:
        """Upload large file using multipart upload"""

        file_size = os.stat(file).st_size

        file_size_gb = file_size / NUM_BYTES_IN_GB
        if file_size_gb > MAX_FILE_SIZE_GB:
            raise FileTypeError(
                f"File size {file_size_gb:.1f}GB exceeds maximum supported size of {MAX_FILE_SIZE_GB}GB"
            )

        part_size, num_parts = self._calculate_parts(file_size)

        file_type = self._get_file_type(file)
        upload_info = None

        try:
            upload_info = self._initiate_upload(
                url, file, file_size, num_parts, purpose, file_type
            )

            completed_parts = self._upload_parts_concurrent(
                file, upload_info, part_size
            )

            return self._complete_upload(
                url, upload_info["upload_id"], upload_info["file_id"], completed_parts
            )

        except Exception as e:
            # Cleanup on failure
            if upload_info is not None:
                self._abort_upload(
                    url, upload_info["upload_id"], upload_info["file_id"]
                )
            raise e

    def _get_file_type(self, file: Path) -> str:
        """Get file type from extension, raising ValueError for unsupported extensions"""
        if file.suffix == ".jsonl":
            return "jsonl"
        elif file.suffix == ".parquet":
            return "parquet"
        elif file.suffix == ".csv":
            return "csv"
        else:
            raise ValueError(
                f"Unsupported file extension: '{file.suffix}'. "
                f"Supported extensions: .jsonl, .parquet, .csv"
            )

    def _calculate_parts(self, file_size: int) -> tuple[int, int]:
        """Calculate optimal part size and count"""
        min_part_size = MIN_PART_SIZE_MB * 1024 * 1024  # 5MB
        target_part_size = TARGET_PART_SIZE_MB * 1024 * 1024  # 100MB

        if file_size <= target_part_size:
            return file_size, 1

        num_parts = min(MAX_MULTIPART_PARTS, math.ceil(file_size / target_part_size))
        part_size = math.ceil(file_size / num_parts)

        if part_size < min_part_size:
            part_size = min_part_size
            num_parts = math.ceil(file_size / part_size)

        return part_size, num_parts

    def _initiate_upload(
        self,
        url: str,
        file: Path,
        file_size: int,
        num_parts: int,
        purpose: FilePurpose,
        file_type: str,
    ) -> Any:
        """Initiate multipart upload with backend"""

        requestor = api_requestor.APIRequestor(client=self._client)

        payload = {
            "file_name": file.name,
            "file_size": file_size,
            "num_parts": num_parts,
            "purpose": purpose.value,
            "file_type": file_type,
        }

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="files/multipart/initiate",
                params=payload,
            ),
        )

        return response.data

    def _upload_parts_concurrent(
        self, file: Path, upload_info: Dict[str, Any], part_size: int
    ) -> List[Dict[str, Any]]:
        """Upload file parts concurrently with progress tracking"""

        parts = upload_info["parts"]
        completed_parts = []

        with ThreadPoolExecutor(max_workers=self.max_concurrent_parts) as executor:
            with tqdm(total=len(parts), desc="Uploading parts", unit="part") as pbar:
                future_to_part = {}

                with open(file, "rb") as f:
                    for part_info in parts:
                        f.seek((part_info["PartNumber"] - 1) * part_size)
                        part_data = f.read(part_size)

                        future = executor.submit(
                            self._upload_single_part, part_info, part_data
                        )
                        future_to_part[future] = part_info["PartNumber"]

                # Collect results
                for future in as_completed(future_to_part):
                    part_number = future_to_part[future]
                    try:
                        etag = future.result()
                        completed_parts.append(
                            {"part_number": part_number, "etag": etag}
                        )
                        pbar.update(1)
                    except Exception as e:
                        raise Exception(f"Failed to upload part {part_number}: {e}")

        completed_parts.sort(key=lambda x: x["part_number"])
        return completed_parts

    def _upload_single_part(self, part_info: Dict[str, Any], part_data: bytes) -> str:
        """Upload a single part and return ETag"""

        response = requests.put(
            part_info["URL"],
            data=part_data,
            headers=part_info.get("Headers", {}),
            timeout=MULTIPART_UPLOAD_TIMEOUT,
        )
        response.raise_for_status()

        etag = response.headers.get("ETag", "").strip('"')
        if not etag:
            raise ResponseError(f"No ETag returned for part {part_info['PartNumber']}")

        return etag

    def _complete_upload(
        self,
        url: str,
        upload_id: str,
        file_id: str,
        completed_parts: List[Dict[str, Any]],
    ) -> FileResponse:
        """Complete the multipart upload"""

        requestor = api_requestor.APIRequestor(client=self._client)

        payload = {
            "upload_id": upload_id,
            "file_id": file_id,
            "parts": completed_parts,
        }

        response, _, _ = requestor.request(
            options=TogetherRequest(
                method="POST",
                url="files/multipart/complete",
                params=payload,
            ),
        )

        return FileResponse(**response.data.get("file", response.data))

    def _abort_upload(self, url: str, upload_id: str, file_id: str) -> None:
        """Abort the multipart upload"""

        requestor = api_requestor.APIRequestor(client=self._client)

        payload = {
            "upload_id": upload_id,
            "file_id": file_id,
        }

        requestor.request(
            options=TogetherRequest(
                method="POST",
                url="files/multipart/abort",
                params=payload,
            ),
        )
