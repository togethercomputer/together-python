import json
import logging
import os
import posixpath
import sys
import urllib.parse
from typing import Dict, List, Optional, Union

import requests
from tqdm import tqdm


DEFAULT_ENDPOINT = "https://api.together.xyz/"


class JSONException(Exception):
    pass


def validate_json(file: str) -> bool:
    with open(file) as f:
        try:
            for line in f:
                json_line = json.loads(line)
                if "text" not in json_line:
                    raise JSONException("Text column not found")
        except ValueError:
            return False
        return True


class Files:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        log_level: str = "WARNING",
    ) -> None:
        self.together_api_key = os.environ.get("TOGETHER_API_KEY", None)
        if self.together_api_key is None:
            raise Exception(
                "TOGETHER_API_KEY not found. Please set it as an environment variable."
            )

        if endpoint_url is None:
            endpoint_url = DEFAULT_ENDPOINT

        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/v1/files/")

        self.logger = logging.getLogger(__name__)

        # Setup logging
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            handlers=[logging.StreamHandler(sys.stdout)],
        )

        self.logger.setLevel(log_level)

    def list_files(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(self.endpoint_url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by files endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

    def upload_file(self, file: str) -> Dict[str, Union[str, int]]:
        try:
            data = {"purpose": "fine-tune", "file_name": os.path.basename(file)}

            headers = {
                "Authorization": f"Bearer {self.together_api_key}",
            }

            if not validate_json(file=file):
                raise ValueError("Could not load file: invalid .jsonl file detected.")

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
            self.logger.debug(f"Response: {response.text}")
            r2_signed_url = response.headers["Location"]
            file_id = response.headers["X-Together-File-Id"]

            self.logger.info(f"R2 Signed URL: {r2_signed_url}")
            self.logger.info("File-ID")

            self.logger.info("Uploading file...")
            # print("> Uploading file...")

            with open(file, "rb") as f:
                response = session.put(r2_signed_url, files={"file": f})

            self.logger.info("> File uploaded.")
            self.logger.debug(f"status code: {response.status_code}")
            self.logger.info("> Processing file...")
            preprocess_url = urllib.parse.urljoin(
                self.endpoint_url, f"{file_id}/preprocess"
            )

            response = session.post(
                preprocess_url,
                headers=headers,
            )

            self.logger.info("> File processed")
            self.logger.debug(f"Status code: {response.status_code}")

        except Exception:
            self.logger.critical("Response error raised.")
            sys.exit(1)

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
            raise ValueError(f"Error raised by files endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

    def retrieve_file(self, file_id: str) -> Dict[str, Union[str, int]]:
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, file_id)
        print(retrieve_url)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by files endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

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
                raise Warning(
                    "Caution: Downloaded file size does not match remote file size."
                )

        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return output  # this should be null
