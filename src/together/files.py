import json
import os
import posixpath
import urllib.parse
from typing import Dict, List, Optional, Union

import requests
import sys
from tqdm import tqdm


DEFAULT_ENDPOINT = "https://api.together.xyz/"


def validate_json(file: str) -> bool:
    with open(file) as f:
        try:
            for line in f:
                json.loads(line)
        except ValueError:
            return False
        return True


class Files:
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
    ) -> None:
        self.together_api_key = os.environ.get("TOGETHER_API_KEY", None)
        if self.together_api_key is None:
            raise Exception(
                "TOGETHER_API_KEY not found. Please set it as an environment variable."
            )

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
            raise ValueError(f"Error raised by inference endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

    def upload_file(self, file: str) -> Dict[str, Union[str, int]]:
        data = {"purpose": "fine-tune", "file_name": os.path.basename(file)}
        print(data)
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        if not validate_json(file=file):
            raise ValueError("Could not load file: invalid .jsonl file detected.")
        # TEMP_URL = "https://47b1b605b8ff0371ec661ebaf3b433c1.r2.cloudflarestorage.com/together-dev//finetune/file-e5731dc6-7e46-4f3a-95c9-4864bd8e19ed?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=257bc5a86d96c8b95a6521e4224f0b18%2F20230705%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20230705T205049Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=9b30c8d69abb9eb959e7b90aa71577af4ff337634f1e7fe5f48d919e701ba889"
        session = requests.Session()
        # send request
        # try:
        response1 = session.post(
                self.endpoint_url, data=data, headers=headers,
            )
        print(response1.text)
        print("Uploading file...")
        r2_signed_url = response1.headers['Location']
        with open(file, "rb") as f:
            response = session.put(
                r2_signed_url, files={"file": f}
            )
        # headers=headers, data=data

        # except (requests.exceptions.RequestException, requests.exceptions.SSLError) as e:
        #     print(f"Error raised by inference endpoint: {e}")
        #     sys.exit(0)

        # try:
        #     response_json = dict(response.json())
        # except Exception:
        print(response.text)
        #     raise ValueError(
        #         f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
        #     )

        # return response_json

    def delete_file(self, file_id: str) -> Dict[str, str]:
        delete_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

    def retrieve_file(self, file_id: str) -> Dict[str, Union[str, int]]:
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

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
