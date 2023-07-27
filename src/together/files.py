import json
import os
import posixpath
import urllib.parse
from logging import Logger
from typing import Dict, List, Union

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

import together
from together import get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)


def validate_file(file: str, logger: Logger) -> bool:
    if not os.path.isfile(file):
        logger.critical("ERROR: File not found")
        return False

    file_size = os.stat(file).st_size

    if file_size > 4.9 * (2**30):
        logger.warning("File size > 4.9 GB, file may fail to upload.")

    with open(file) as f:
        try:
            for line in f:
                json_line = json.loads(line)
                if "text" not in json_line:
                    logger.critical(
                        "ERROR: 'text' field not found in one or more lines in JSONL file"
                    )
                    return False
        except ValueError:
            logger.critical("ERROR: Could not load JSONL file. Invalid format")
            return False
        return True


class Files:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

    @classmethod
    def list(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.get(together.api_base_files, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)
        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def upload(self, file: str) -> Dict[str, Union[str, int]]:
        data = {"purpose": "fine-tune", "file_name": os.path.basename(file)}

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        if not validate_file(file=file, logger=logger):
            raise together.FileTypeError("Invalid file supplied. Failed to upload.")

        session = requests.Session()

        init_endpoint = together.api_base_files[:-1]

        logger.debug(
            f"Upload file POST request: data={data}, headers={headers}, URL={init_endpoint}, allow_redirects=False"
        )
        try:
            response = session.post(
                init_endpoint,
                data=data,
                headers=headers,
                allow_redirects=False,
            )

            logger.debug(f"Response text: {response.text}")
            logger.debug(f"Response header: {response.headers}")
            logger.debug(f"Response status code: {response.status_code}")

            if response.status_code == 401:
                logger.critical(
                    "This job would exceed your free trial credits. Please upgrade to a paid account through Settings -> Billing on api.together.ai to continue."
                )
                raise together.AuthenticationError(
                    "This job would exceed your free trial credits. Please upgrade to a paid account through Settings -> Billing on api.together.ai to continue."
                )
            elif response.status_code != 302:
                logger.critical(
                    f"Unexpected error raised by endpoint. Response status code: {response.status_code}"
                )
                raise together.ResponseError(
                    "Unexpected error raised by endpoint.",
                    http_status=response.status_code,
                )

            r2_signed_url = response.headers["Location"]
            file_id = response.headers["X-Together-File-Id"]

            logger.info(f"R2 Signed URL: {r2_signed_url}")
            logger.info("File-ID")

            logger.info("Uploading file...")

            file_size = os.stat(file).st_size
            progress_bar = tqdm(
                total=file_size, unit="B", unit_scale=True, unit_divisor=1024
            )
            progress_bar.set_description(f"Uploading {file}")
            with open(file, "rb") as f:
                wrapped_file = CallbackIOWrapper(progress_bar.update, f, "read")
                response = requests.put(r2_signed_url, data=wrapped_file)
                response.raise_for_status()

            logger.info("File uploaded.")
            logger.debug(f"status code: {response.status_code}")
            logger.info("Processing file...")
            preprocess_url = urllib.parse.urljoin(
                together.api_base_files, f"{file_id}/preprocess"
            )

            response = session.post(
                preprocess_url,
                headers=headers,
            )

            logger.info("File processed")
            logger.debug(f"Status code: {response.status_code}")

        except Exception as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        return {
            "filename": os.path.basename(file),
            "id": str(file_id),
            "object": "file",
        }

    @classmethod
    def delete(self, file_id: str) -> Dict[str, str]:
        delete_url = urllib.parse.urljoin(together.api_base_files, file_id)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def retrieve(self, file_id: str) -> Dict[str, Union[str, int]]:
        retrieve_url = urllib.parse.urljoin(together.api_base_files, file_id)

        logger.info(f"Retrieve URL: {retrieve_url}")

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def retrieve_content(self, file_id: str, output: Union[str, None] = None) -> str:
        if output is None:
            output = file_id + ".jsonl"

        relative_path = posixpath.join(file_id, "content")
        retrieve_url = urllib.parse.urljoin(together.api_base_files, relative_path)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            session = requests.Session()

            response = session.get(retrieve_url, headers=headers, stream=True)
            response.raise_for_status()

            total_size_in_bytes = int(response.headers.get("content-length", 0))
            block_size = 1024 * 1024  # 1 MB
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
            progress_bar.set_description(f"Downloading {output}")

            with open(output, "wb") as file:
                for chunk in response.iter_content(block_size):
                    progress_bar.update(len(chunk))
                    file.write(chunk)

            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                logger.warning(
                    "Caution: Downloaded file size does not match remote file size."
                )

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        return output  # this should be null
