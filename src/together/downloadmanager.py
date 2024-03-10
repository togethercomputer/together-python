from __future__ import annotations

import os
import shutil
import stat
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    DOWNLOAD_CONCURRENCY,
    MAX_CONNECTION_RETRIES,
)
from together.error import DownloadError, FileTypeError
from together.types import TogetherClient, TogetherRequest
from together.utils import log_warn


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


def download_part(
    requestor: api_requestor.APIRequestor,
    url: str,
    start_byte: int,
    end_byte: int,
    local_file: str = "",
    first_chunk: bool = False,
) -> CaseInsensitiveDict[str] | None:
    """
    Multi-part download helper - downloads part of a remote file
    """

    retries = MAX_CONNECTION_RETRIES

    while retries > 0:
        try:
            response, _, _ = requestor.request(
                options=TogetherRequest(
                    method="GET",
                    url=url,
                    headers={"Range": f"bytes={start_byte}-{end_byte}"},
                ),
                stream=False,
                return_raw=True,
            )

            if first_chunk:
                return response.headers

            with open(local_file, "rb+") as f:
                f.seek(start_byte)
                f.write(response.content)

            return None

        except Exception:
            log_warn(
                f"Error downloading part {start_byte}-{end_byte} of {url}. Retries left: {retries}"
            )

            retries -= 1

    raise Exception(
        f"Error downloading part {start_byte}-{end_byte} of {url}. Tried {retries} times."
    )


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
        output: str | None = None,
        remote_name: str | None = None,
    ) -> Path:
        """
        Generates output file name from remote name and headers
        """
        if output:
            return Path(output)

        content_type = str(headers.get("content-type"))

        assert remote_name, (
            "No model name found in fine_tune object. "
            "Please specify an `output` file name."
        )

        output = remote_name.split("/")[1]

        if step > 0:
            output += f"-checkpoint-{step}"

        if "x-tar" in content_type.lower():
            output += ".tar.gz"

        elif "zstd" in content_type.lower() or step != -1:
            output += ".tar.zst"

        else:
            raise FileTypeError(
                f"Unknown file type {content_type} found. Aborting download."
            )

        return Path(output)

    def get_file_metadata(
        self, url: str, output: str | None = None, remote_name: str | None = None
    ) -> Tuple[Path, int]:
        """
        gets remote file head and parses out file name and file size
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        headers = download_part(
            requestor=requestor,
            url=url,
            start_byte=0,
            end_byte=1,
            first_chunk=True,
        )

        assert isinstance(headers, CaseInsensitiveDict)

        file_path = self._prepare_output(
            headers=headers,
            output=output,
            remote_name=remote_name,
        )

        file_size = self._get_file_size(headers)

        return file_path, file_size

    def download(
        self, url: str, output: str | None = None, remote_name: str | None = None
    ) -> Tuple[Path, int]:
        """
        Multi-part download method from remote HTTP endpoint.
        Downloads data to a temp file with a lock with concurrency and
        chunk size defined in together.constants.
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        file_path, file_size = self.get_file_metadata(url, output, remote_name)

        temp_file_manager = partial(
            tempfile.NamedTemporaryFile, mode="wb", dir=file_path.parent, delete=False
        )

        # Prevent parallel downloads of the same file with a lock.
        lock_path = file_path.with_suffix(".lock")

        # layered with-as statements instead of using grouping parentheses for python<3.10
        # https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
        with ThreadPoolExecutor(max_workers=DOWNLOAD_CONCURRENCY) as executor:
            with FileLock(lock_path):
                with temp_file_manager() as temp_file:
                    futures = []

                    start_byte = 0

                    while start_byte < file_size:
                        end_byte = min(
                            start_byte + DOWNLOAD_BLOCK_SIZE - 1, file_size - 1
                        )

                        futures.append(
                            executor.submit(
                                download_part,
                                requestor,
                                url,
                                start_byte,
                                end_byte,
                                temp_file.name,
                            )
                        )

                        start_byte = end_byte + 1

                    with tqdm(
                        total=file_size,
                        unit="B",
                        unit_scale=True,
                        desc=f"Downloading file {file_path.name}",
                        disable=bool(DISABLE_TQDM),
                    ) as pbar:
                        for future in as_completed(futures):
                            pbar.update(DOWNLOAD_BLOCK_SIZE)

        executor.shutdown()

        # Raise exception if remote file size does not match downloaded file size
        if os.stat(temp_file).st_size != file_size:
            DownloadError(
                f"Downloaded file size `{pbar.n}` bytes does not match "
                f"remote file size `{file_size}` bytes."
            )

        # Moves temp file to output file path
        chmod_and_replace(Path(temp_file.name), file_path)

        return file_path, file_size
