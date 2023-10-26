import posixpath
import pprint
import urllib.parse
from typing import Any, Dict, List, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util import Retry

import together
from together import Files
from together.utils import (
    create_get_request,
    create_post_request,
    get_logger,
    response_to_dict,
    round_to_closest_multiple_of_32,
)


pp = pprint.PrettyPrinter(indent=4)

logger = get_logger(str(__name__))


class Finetune:
    # TODO @orangetin: cleanup create validation etc
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
        estimate_price: bool = False,
        wandb_api_key: Optional[str] = None,
        confirm_inputs: bool = False,
    ) -> Dict[Any, Any]:
        adjusted_inputs = False

        if n_epochs is None or n_epochs < 1:
            n_epochs = 1
            adjusted_inputs = True

        # Validate parameters
        if n_checkpoints is None:
            n_checkpoints = 1
        elif n_checkpoints < 1:
            n_checkpoints = 1
            adjusted_inputs = True
        elif n_checkpoints > n_epochs:
            n_checkpoints = n_epochs
            adjusted_inputs = True

        # TODO: Replace with mongodb retrieval for max, min, and default batch size
        if batch_size is None:
            batch_size = 32
        elif batch_size < 4:
            batch_size = 4
            adjusted_inputs = True

        max_batch_size = 128
        if model.startswith("togethercomputer/llama-2-70b"):
            max_batch_size = 64
            batch_size = round_to_closest_multiple_of_32(batch_size)
            adjusted_inputs = True
        elif model.startswith("togethercomputer/CodeLlama-7b"):
            max_batch_size = 16
        elif model.startswith("togethercomputer/CodeLlama-13b"):
            max_batch_size = 8

        if batch_size > max_batch_size:
            batch_size = max_batch_size
            adjusted_inputs = True

        # TODO: REMOVE THIS CHECK WHEN WE HAVE CHECKPOINTING WORKING FOR 70B models
        if n_checkpoints > 1 and model in [
            "togethercomputer/llama-2-70b",
            "togethercomputer/llama-2-70b-chat",
        ]:
            n_checkpoints = 1
            adjusted_inputs = True

        parameter_payload = {
            "training_file": training_file,
            # "validation_file": validation_file,
            "model": model,
            "n_epochs": n_epochs,
            "n_checkpoints": n_checkpoints,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            # "warmup_steps": warmup_steps,
            # "train_warmup_steps": train_warmup_steps,
            # "seq_length": seq_length,
            # "seed": seed,
            # "fp16": fp16,
            "suffix": suffix,
            "wandb_key": wandb_api_key,
        }

        # check if model name is one of the models available for finetuning
        if not together.Models._is_finetune_model(model):
            raise ValueError(
                "The finetune model name must be one of the subset of models available for finetuning. "
                "Here is a list of those models https://docs.together.ai/docs/models-fine-tuning"
            )

        # check if training_file is the string id of a previously uploaded file
        uploaded_files = Files.list()
        file_ids = [f["id"] for f in uploaded_files["data"]]
        if parameter_payload["training_file"] not in file_ids:
            training_file_feedback = (
                "training_file refers to a file identifier of an uploaded training file, not a local file path. "
                "A list of uploaded files and file identifiers can be retrieved with `together.Files.list()` Python API or "
                "$ together files list` CLI. A training file can be uploaded using `together.Files.upload(file ='/path/to/file')"
                "Python API or `$ together files upload <FILE_PATH>` CLI."
            )
            logger.critical(training_file_feedback)
            raise together.FileTypeError(training_file_feedback)

        if estimate_price:
            param_size = together.Models._param_count(model)
            if param_size == 0:
                error = f"Unknown model {model}.  Cannot estimate price.  Please check the name of the model"
                raise together.FileTypeError(error)

            for file in uploaded_files["data"]:
                if file["id"] == parameter_payload["training_file"]:
                    ## This is the file
                    byte_count = file["bytes"]
                    token_estimate = int(int(file["bytes"]) / 4)
                    data = {
                        "method": "together_getPrice",
                        "params": [
                            model,
                            "FT",
                            {
                                "tokens": token_estimate,
                                "epochs": n_epochs,
                                "parameters": together.Models._param_count(model),
                            },
                        ],
                        "id": 1,
                    }
                    r = requests.post("https://computer.together.xyz/", json=data)
                    estimate = r.json()["result"]["total"]
                    estimate /= 1000000000
                    training_file_feedback = f"A rough price estimate for this job is ${estimate:.2f} USD. The estimated number of tokens is {token_estimate} tokens. Accurate pricing is not available until full tokenization has been performed. The actual price might be higher or lower depending on how the data is tokenized. Our token estimate is based on the number of bytes in the training file, {byte_count} bytes, divided by an average token length of 4 bytes. We currently have a per job minimum of $5.00 USD."
                    print(training_file_feedback)
                    exit()

        if confirm_inputs:
            if adjusted_inputs:
                print(
                    "Note: Some hyperparameters have been adjusted with their minimum/maximum values for a given model."
                )
            print("Job creation details:")
            pp.pprint(parameter_payload)
            confirm_response = input("\nDo you want to submit the job? [y/N]")
            if "y" not in confirm_response.lower():
                return {"status": "job not submitted"}

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
