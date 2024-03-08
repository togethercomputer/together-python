import posixpath
import urllib.parse
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util import Retry

import together
from together.utils import (
    create_get_request,
    create_post_request,
    get_logger,
    response_to_dict,
)


logger = get_logger(str(__name__))


class Finetune:
    @classmethod
    def create(
        self,
        training_file: str,  # training file_id
        model: str,
        n_epochs: int = 1,
        n_checkpoints: Optional[int] = 1,
        batch_size: Optional[int] = 32,
        learning_rate: Optional[float] = 0.00001,
        suffix: Optional[
            str
        ] = None,  # resulting finetuned model name will include the suffix
        wandb_api_key: Optional[str] = None,
    ) -> Dict[Any, Any]:
        parameter_payload = {
            "training_file": training_file,
            "model": model,
            "n_epochs": n_epochs,
            "n_checkpoints": n_checkpoints,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "suffix": suffix,
            "wandb_key": wandb_api_key,
        }

        # Send POST request to SUBMIT FINETUNE JOB
        response = create_post_request(
            together.api_base_finetune, json=parameter_payload
        )

        return response_to_dict(response)

    @classmethod
    def list(self) -> Dict[str, List[Dict[str, Any]]]:
        # send request
        response = create_get_request(together.api_base_finetune)

        return response_to_dict(response)

    @classmethod
    def retrieve(self, fine_tune_id: str) -> Dict[str, Any]:
        retrieve_url = urllib.parse.urljoin(together.api_base_finetune, fine_tune_id)
        response = create_get_request(retrieve_url)

        return response_to_dict(response)

    @classmethod
    def cancel(self, fine_tune_id: str) -> Dict[Any, Any]:
        relative_path = posixpath.join(fine_tune_id, "cancel")
        retrieve_url = urllib.parse.urljoin(together.api_base_finetune, relative_path)
        response = create_post_request(retrieve_url)

        return response_to_dict(response)

    @classmethod
    def list_events(self, fine_tune_id: str) -> Dict[Any, Any]:
        # TODO enable stream
        relative_path = posixpath.join(fine_tune_id, "events")
        retrieve_url = urllib.parse.urljoin(together.api_base_finetune, relative_path)
        response = create_get_request(retrieve_url)

        return response_to_dict(response)

    @classmethod
    def get_checkpoints(self, fine_tune_id: str) -> List[Dict[str, Any]]:
        try:
            finetune_events = list(self.retrieve(fine_tune_id=fine_tune_id)["events"])
        except Exception as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        saved_events = [i for i in finetune_events if i["type"] in ["CHECKPOINT_SAVE"]]

        return saved_events

    @classmethod
    def get_job_status(self, fine_tune_id: str) -> str:
        try:
            job_status = str(self.retrieve(fine_tune_id=fine_tune_id)["status"])
        except Exception as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        return job_status

    @classmethod
    def is_final_model_available(self, fine_tune_id: str) -> bool:
        try:
            finetune_events = list(self.retrieve(fine_tune_id=fine_tune_id)["events"])
        except Exception as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        for i in finetune_events:
            if i["type"] in ["JOB_COMPLETE", "JOB_ERROR"]:
                if i["checkpoint_path"] != "":
                    return False
                else:
                    return True
        return False

    @classmethod
    def download(
        self,
        fine_tune_id: str,
        output: Union[str, None] = None,
        step: int = -1,
    ) -> str:
        # default to model_output_path name
        model_file_path = urllib.parse.urljoin(
            together.api_base_finetune,
            f"/api/finetune/downloadfinetunefile?ft_id={fine_tune_id}",
        )
        if step != -1:
            model_file_path += f"&checkpoint_step={step}"

        print(f"Downloading weights from {model_file_path}...")

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        session = requests.Session()

        retry_strategy = Retry(
            total=together.MAX_CONNECTION_RETRIES,
            backoff_factor=together.BACKOFF_FACTOR,
        )
        retry_adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", retry_adapter)

        try:
            response = session.get(model_file_path, headers=headers, stream=True)
            response.raise_for_status()

            if output is None:
                content_type = str(response.headers.get("content-type"))

                output = self.retrieve(fine_tune_id)["model_output_name"].split("/")[-1]

                if step != -1:
                    output += f"-checkpoint-{step}"

                if "x-tar" in content_type.lower():
                    output += ".tar.gz"
                elif "zstd" in content_type.lower() or step != -1:
                    output += ".tar.zst"
                else:
                    raise together.ResponseError(
                        f"Unknown file type {content_type} found. Aborting download."
                    )

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
            raise together.ResponseError(e)
        finally:
            session.close()

        return output  # this should be output file name
