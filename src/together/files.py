import json
import os
import posixpath
import urllib.parse
from typing import Dict, List, Optional, Union

import requests


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
        data = {"purpose": "fine-tune"}
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        if not validate_json(file=file):
            raise ValueError("Could not load file: invalid .jsonl file detected.")

        # send request
        try:
            with open(file, "rb") as f:
                response = requests.post(
                    self.endpoint_url, headers=headers, files={"file": f}, data=data
                )

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

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

    def retrieve_file_content(self, file_id: str) -> requests.Response:
        relative_path = posixpath.join(file_id, "content")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response  # this should be null
