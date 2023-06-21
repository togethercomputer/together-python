import os
import posixpath
import urllib.parse
from typing import Any, Dict, Optional

import requests


DEFAULT_ENDPOINT = "https://api.together.xyz/"


class Finetune:
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

        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/v1/fine-tunes/")

    def create_finetune(
        self,
        training_file: str,  # training file_id
        validation_file: Optional[str] = None,  # validation file_id
        model: Optional[str] = None,
        n_epochs: Optional[int] = 1,
        batch_size: Optional[int] = 32,
        learning_rate: Optional[float] = 0.00001,
        warmup_steps: Optional[int] = 0,
        train_warmup_steps: Optional[int] = 0,
        seq_length: Optional[int] = 2048,
        seed: Optional[int] = 42,
        fp16: Optional[bool] = True,
        suffix: Optional[str] = None,
    ) -> Dict[Any, Any]:
        parameter_payload = {
            "training_file": training_file,
            "validation_file": validation_file,
            "model": model,
            "n_epochs": n_epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "warmup_steps": warmup_steps,
            "train_warmup_steps": train_warmup_steps,
            "seq_length": seq_length,
            "seed": seed,
            "fp16": fp16,
            "suffix": suffix,
        }

        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json",
        }

        # send request
        try:
            response = requests.post(
                self.endpoint_url, headers=headers, json=parameter_payload
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

    def list_finetune(self) -> Dict[Any, Any]:
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

    def retrieve_finetune(self, fine_tune_id: str) -> Dict[Any, Any]:
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, fine_tune_id)

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

    def cancel_finetune(self, fine_tune_id: str) -> Dict[Any, Any]:
        relative_path = posixpath.join(fine_tune_id, "cancel")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        # send request
        try:
            response = requests.post(retrieve_url, headers=headers)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error raised by inference endpoint: {e}")

        try:
            response_json = dict(response.json())
        except Exception:
            raise ValueError(
                f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
            )

        return response_json

    def list_finetune_events(self, fine_tune_id: str) -> Dict[Any, Any]:
        # TODO enable stream
        relative_path = posixpath.join(fine_tune_id, "events")
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, relative_path)

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

    # def delete_finetune_model(self, model: str) -> Dict[Any, Any]:
    #     model_url = "https://api.together.xyz/api/models"
    #     delete_url = urllib.parse.urljoin(model_url, model)

    #     headers = {
    #         "Authorization": f"Bearer {self.together_api_key}",
    #     }

    #     # send request
    #     try:
    #         response = requests.delete(delete_url, headers=headers)
    #     except requests.exceptions.RequestException as e:
    #         raise ValueError(f"Error raised by inference endpoint: {e}")

    #     try:
    #         response_json = dict(response.json())
    #     except Exception as e:
    #         raise ValueError(
    #             f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
    #         )

    #     return response_json
