import os
import posixpath
import urllib.parse
from typing import Any, Dict, List, Optional

import requests
from tqdm import tqdm


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
        n_epochs: Optional[int] = 4,
        batch_size: Optional[int] = None,
        learning_rate_multiplier: Optional[float] = None,
        prompt_loss_weight: Optional[float] = 0.01,
        compute_classification_metrics: Optional[bool] = False,
        classification_n_classes: Optional[int] = None,
        classification_positive_class: Optional[str] = None,
        classification_betas: Optional[List[Any]] = None,
        suffix: Optional[str] = None,
    ) -> Dict[Any, Any]:
        parameter_payload = {
            "training_file": training_file,
            "validation_file": validation_file,
            "model": model,
            "n_epochs": n_epochs,
            "batch_size": batch_size,
            "learning_rate_multiplier": learning_rate_multiplier,
            "prompt_loss_weight": prompt_loss_weight,
            "compute_classification_metrics": compute_classification_metrics,
            "classification_n_classes": classification_n_classes,
            "classification_positive_class": classification_positive_class,
            "classification_betas": classification_betas,
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

    def get_checkpoints(self, fine_tune_id: str) -> List[Dict[str, Any]]:
        try:
            finetune_events = list(
                self.retrieve_finetune(fine_tune_id=fine_tune_id)["events"]
            )
        except Exception as e:
            raise ValueError(f"Error: Failed to retrieve fine tune events: {e}")

        saved_events = [i for i in finetune_events if i["type"] in ["CHECKPOINT_SAVE"]]

        return saved_events

    def get_job_status(self, fine_tune_id: str) -> str:
        try:
            job_status = str(
                self.retrieve_finetune(fine_tune_id=fine_tune_id)["status"]
            )
        except Exception as e:
            raise ValueError(f"Error: Failed to retrieve fine tune events: {e}")

        return job_status

    def is_final_model_available(self, fine_tune_id: str) -> bool:
        try:
            finetune_events = list(
                self.retrieve_finetune(fine_tune_id=fine_tune_id)["events"]
            )
        except Exception as e:
            raise ValueError(f"Error: Failed to retrieve fine tune events: {e}")

        for i in finetune_events:
            if i["type"] in ["JOB_COMPLETE", "JOB_ERROR"]:
                if i["checkpoint_path"] != "":
                    return False
                else:
                    return True
        return False

    def download(self, fine_tune_id: str, output: str, checkpoint_num: int = -1) -> str:
        model_file_path = urllib.parse.urljoin(
            self.endpoint_url,
            f"/api/finetune/downloadfinetunefile?ft_id={fine_tune_id}",
        )

        print(f"Downloading {model_file_path}...")

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
        }

        try:
            session = requests.Session()

            response = session.get(model_file_path, headers=headers, stream=True)
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
