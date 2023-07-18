import os
import posixpath
import urllib.parse
from typing import Any, Dict, List, Optional, Union

import requests
from tqdm import tqdm

from together.utils.utils import exit_1, get_logger


DEFAULT_ENDPOINT = "https://api.together.xyz/"


class Finetune:
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

        self.endpoint_url = urllib.parse.urljoin(endpoint_url, "/v1/fine-tunes/")

    def create_finetune(
        self,
        training_file: str,  # training file_id
        # validation_file: Optional[str] = None,  # validation file_id
        model: Optional[str] = None,
        n_epochs: Optional[int] = 1,
        batch_size: Optional[int] = 32,
        learning_rate: Optional[float] = 0.00001,
        # warmup_steps: Optional[int] = 0,
        # train_warmup_steps: Optional[int] = 0,
        # seq_length: Optional[int] = 2048,
        # seed: Optional[int] = 42,
        # fp16: Optional[bool] = True,
        # checkpoint_steps: Optional[int] = None,
        suffix: Optional[str] = None,
    ) -> Dict[Any, Any]:
        parameter_payload = {
            "training_file": training_file,
            # "validation_file": validation_file,
            "model": model,
            "n_epochs": n_epochs,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            # "warmup_steps": warmup_steps,
            # "train_warmup_steps": train_warmup_steps,
            # "seq_length": seq_length,
            # "seed": seed,
            # "fp16": fp16,
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

    def list_finetune(self) -> Dict[Any, Any]:
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

    def retrieve_finetune(self, fine_tune_id: str) -> Dict[Any, Any]:
        retrieve_url = urllib.parse.urljoin(self.endpoint_url, fine_tune_id)

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

    def get_checkpoints(self, fine_tune_id: str) -> List[Dict[str, Any]]:
        try:
            finetune_events = list(
                self.retrieve_finetune(fine_tune_id=fine_tune_id)["events"]
            )
        except Exception as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        saved_events = [i for i in finetune_events if i["type"] in ["CHECKPOINT_SAVE"]]

        return saved_events

    def get_job_status(self, fine_tune_id: str) -> str:
        try:
            job_status = str(
                self.retrieve_finetune(fine_tune_id=fine_tune_id)["status"]
            )
        except Exception as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        return job_status

    def is_final_model_available(self, fine_tune_id: str) -> bool:
        try:
            finetune_events = list(
                self.retrieve_finetune(fine_tune_id=fine_tune_id)["events"]
            )
        except Exception as e:
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

        for i in finetune_events:
            if i["type"] in ["JOB_COMPLETE", "JOB_ERROR"]:
                if i["checkpoint_path"] != "":
                    return False
                else:
                    return True
        return False

    def download(
        self,
        fine_tune_id: str,
        output: Union[str, None] = None,
        checkpoint_num: int = -1,
    ) -> str:
        # default to model_output_path name
        if output is None:
            output = (
                self.retrieve_finetune(fine_tune_id)["model_output_path"].split("/")[-1]
                + ".tar.gz"
            )

        model_file_path = urllib.parse.urljoin(
            self.endpoint_url,
            f"/api/finetune/downloadfinetunefile?ft_id={fine_tune_id}",
        )

        self.logger.info(f"Downloading {model_file_path}...")

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
                self.logger.warning(
                    "Caution: Downloaded file size does not match remote file size."
                )
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            self.logger.critical(f"Response error raised: {e}")
            exit_1(self.logger)

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
    #         raise ValueError(f"Error raised by finetune endpoint: {e}")

    #     try:
    #         response_json = dict(response.json())
    #     except Exception as e:
    #         raise ValueError(
    #             f"JSON Error raised. \nResponse status code: {str(response.status_code)}"
    #         )

    #     return response_json
