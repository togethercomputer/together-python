import argparse
import json
import os
import posixpath
import urllib.parse
from typing import Any, Dict, Optional

import requests


DEFAULT_ENDPOINT = "https://api.together.xyz/"


def dispatch_files(args: argparse.Namespace) -> None:
    files = Files(args.key)

    if args.files == "list_files":
        response = files.list_files()
        print(response)

    elif args.files == "upload_file":
        response = files.upload_file(args.file)
        print(response)

    elif args.files == "delete_file":
        response = files.delete_file(args.file_id)
        print(response)

    elif args.files == "retrieve_file":
        response = files.retrieve_file(args.file_id)
        print(response)

    elif args.files == "retrieve_file_content":
        response = files.retrieve_file_content(args.file_id, args.output)
        print(response)


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

    def list_files(self) -> Dict[Any, Any]:
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = dict(requests.get(self.endpoint_url, headers=headers).json())
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def upload_file(self, file: str) -> Dict[Any, Any]:
        data = {"purpose": "fine-tune"}
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        if not validate_json(file=file):
            raise ValueError("Could not load file: invalid .jsonl file detected.")

        # send request
        try:
            with open(file, "rb") as f:
                response = dict(
                    requests.post(
                        self.endpoint_url, headers=headers, files={"file": f}, data=data
                    ).json()
                )
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def delete_file(self, file_id: str) -> Dict[Any, Any]:
        delete_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = dict(requests.delete(delete_url, headers=headers).json())
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_file(self, file_id: str) -> Dict[Any, Any]:
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, file_id)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = dict(requests.get(retrieve_url, headers=headers).json())
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise ValueError(f"Error raised by endpoint: {e}")

        return response

    def retrieve_file_content(self, file_id: str, output_file: str) -> Any:
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

        # write to file
        open(output_file, "wb").write(response.content)

        return response  # this should be null
