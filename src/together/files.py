import json
import os
import posixpath
import urllib.parse
from logging import Logger
from typing import Dict, List, Optional, Union

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from together.utils.utils import exit_1, get_logger


DEFAULT_ENDPOINT = "https://api.together.xyz/"


class JSONException(Exception):
    pass


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
        endpoint_url: Optional[str] = None,
        log_level: str = "WARNING",
    ) -> None:
        # Setup logger
        self.logger = get_logger(__name__, log_level=log_level)

        self.together_api_key = os.environ.get("TOGETHER_API_KEY", None)
        if self.together_api_key is None:
            self.logger.critical(
                "TOGETHER_API_KEY not found. Please set it as an environment variable."
            )
            exit_1(self.logger)

        if endpoint_url is None:
            endpoint_url = DEFAULT_ENDPOINT

        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/v1/files/")

    def list_files(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(self.endpoint_url, headers=headers)
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)
        try:
            response_json = dict(response.json())
        except Exception as e:
            self.logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(self.logger)

        return response_json

    def upload_file(self, file: str) -> Dict[str, Union[str, int]]:
        try:
            data = {"purpose": "fine-tune", "file_name": os.path.basename(file)}

            headers = {
                "Authorization": f"Bearer {self.together_api_key}",
            }

            if not validate_file(file=file, logger=self.logger):
                exit_1(self.logger)

            session = requests.Session()

            init_endpoint = self.endpoint_url[:-1]

            self.logger.debug(
                f"Upload file POST request: data={data}, headers={headers}, URL={init_endpoint}, allow_redirects=False"
            )

            response = session.post(
                init_endpoint,
                data=data,
                headers=headers,
                allow_redirects=False,
            )

            self.logger.debug(f"Response text: {response.text}")
            self.logger.debug(f"Response header: {response.headers}")
            self.logger.debug(f"Response status code: {response.status_code}")

            if response.status_code == 401:
                self.logger.critical(
                    "This job would exceed your free trial credits. Please upgrade to a paid account through Settings -> Billing on api.together.ai to continue."
                )
                exit_1(self.logger)
            elif response.status_code != 302:
                self.logger.critical(
                    f"Unexpected error raised by endpoint. Response status code: {response.status_code}"
                )
                exit_1(self.logger)

            r2_signed_url = response.headers["Location"]
            file_id = response.headers["X-Together-File-Id"]

            self.logger.info(f"R2 Signed URL: {r2_signed_url}")
            self.logger.info("File-ID")

            self.logger.info("Uploading file...")

            file_size = os.stat(file).st_size
            with open(file, "rb") as f:
                with tqdm(
                    total=file_size, unit="B", unit_scale=True, unit_divisor=1024
                ) as t:
                    wrapped_file = CallbackIOWrapper(t.update, f, "read")
                    response = requests.put(r2_signed_url, data=wrapped_file)

            self.logger.info("File uploaded.")
            self.logger.debug(f"status code: {response.status_code}")
            self.logger.info("Processing file...")
            preprocess_url = urllib.parse.urljoin(
                self.endpoint_url, f"{file_id}/preprocess"
            )

            response = session.post(
                preprocess_url,
                headers=headers,
            )

            self.logger.info("File processed")
            self.logger.debug(f"Status code: {response.status_code}")

        except Exception as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        return {
            "filename": os.path.basename(file),
            "id": str(file_id),
            "object": "file",
        }

    def delete_file(self, file_id: str) -> Dict[str, str]:
        delete_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers)
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        try:
            response_json = dict(response.json())
        except Exception as e:
            self.logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(self.logger)

        return response_json

    def retrieve_file(self, file_id: str) -> Dict[str, Union[str, int]]:
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        self.logger.info(f"Retrieve URL: {retrieve_url}")

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        try:
            response_json = dict(response.json())
        except Exception as e:
            self.logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            exit_1(self.logger)

        return response_json

    def retrieve_file_content(
        self, file_id: str, output: Union[str, None] = None
    ) -> str:
        if output is None:
            output = file_id + ".jsonl"

        relative_path = posixpath.join(file_id, "content")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            session = requests.Session()

            response = session.get(retrieve_url, headers=headers, stream=True)
            response.raise_for_status()

            total_size_in_bytes = int(response.headers.get("content-length", 0))
            block_size = 1024 * 1024  # 1 MB
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

            with open(output, "wb") as file:
                for chunk in response.iter_content(block_size):
                    progress_bar.update(len(chunk))
                    file.write(chunk)

            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                self.logger.warning(
                    "Caution: Downloaded file size does not match remote file size."
                )

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        return output  # this should be null
