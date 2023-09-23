import posixpath
import urllib.parse
from typing import Any, Dict, List, Optional, Union

import requests
from tqdm import tqdm

import together
from together import Files
from together.utils.utils import get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)


# this will change soon to be data driven and give a clearer estimate
def model_param_count(name: str) -> int:
    pcount = {
        "togethercomputer/RedPajama-INCITE-7B-Chat": 6857302016,
        "togethercomputer/RedPajama-INCITE-7B-Base": 6857302016,
        "togethercomputer/RedPajama-INCITE-7B-Instruct": 6857302016,
        "togethercomputer/RedPajama-INCITE-Chat-3B-v1": 2775864320,
        "togethercomputer/RedPajama-INCITE-Base-3B-v1": 2775864320,
        "togethercomputer/RedPajama-INCITE-Instruct-3B-v1": 2775864320,
        "togethercomputer/Pythia-Chat-Base-7B": 6857302016,
        "togethercomputer/llama-2-7b": 6738415616,
        "togethercomputer/llama-2-7b-chat": 6738415616,
        "togethercomputer/llama-2-13b": 13015864320,
        "togethercomputer/llama-2-13b-chat": 13015864320,
        "togethercomputer/LLaMA-2-7B-32K": 6738415616,
        "togethercomputer/Llama-2-7B-32K-Instruct": 6738415616,
        "togethercomputer/CodeLlama-7b": 6738546688,
        "togethercomputer/CodeLlama-7b-Python": 6738546688,
        "togethercomputer/CodeLlama-7b-Instruct": 6738546688,
        "togethercomputer/CodeLlama-13b": 13016028160,
        "togethercomputer/CodeLlama-13b-Python": 13016028160,
        "togethercomputer/CodeLlama-13b-Instruct": 13016028160,
        "togethercomputer/llama-2-70b": 68976648192,
        "togethercomputer/llama-2-70b-chat": 68976648192,
    }
    try:
        return pcount[name]
    except Exception:
        return 0


class Finetune:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

    @classmethod
    def create(
        self,
        training_file: str,  # training file_id
        # validation_file: Optional[str] = None,  # validation file_id
        model: str,
        n_epochs: int = 1,
        n_checkpoints: Optional[int] = 1,
        batch_size: Optional[int] = 32,
        learning_rate: Optional[float] = 0.00001,
        # warmup_steps: Optional[int] = 0,
        # train_warmup_steps: Optional[int] = 0,
        # seq_length: Optional[int] = 2048,
        # seed: Optional[int] = 42,
        # fp16: Optional[bool] = True,
        # checkpoint_steps: Optional[int] = None,
        suffix: Optional[
            str
        ] = None,  # resulting finetuned model name will include the suffix
        estimate_price: bool = False,
        wandb_api_key: Optional[str] = None,
    ) -> Dict[Any, Any]:
        if n_epochs is None or n_epochs < 1:
            logger.fatal("The number of epochs must be specified")
            raise ValueError("n_epochs is required")

        # Validate parameters
        if n_checkpoints is None:
            n_checkpoints = 1
        elif n_checkpoints < 1:
            n_checkpoints = 1
            logger.warning(
                f"The number of checkpoints must be >= 1, setting to {n_checkpoints}"
            )
        elif n_checkpoints > n_epochs:
            n_checkpoints = n_epochs
            logger.warning(
                f"The number of checkpoints must be < the number of epochs, setting to {n_checkpoints}"
            )

        if (
            model
            in ["togethercomputer/llama-2-70b", "togethercomputer/llama-2-70b-chat"]
            and batch_size != 144
        ):
            raise ValueError(
                f"Batch size must be 144 for {model} model. Please set batch size to 144"
            )

        if batch_size is None:
            batch_size = 32
        elif batch_size < 4:
            raise ValueError("Batch size must be >= 4.")

        # TODO: REMOVE THIS CHECK WHEN WE HAVE CHECKPOINTING WORKING FOR 70B models
        if n_checkpoints > 1 and model in [
            "togethercomputer/llama-2-70b",
            "togethercomputer/llama-2-70b-chat",
        ]:
            raise ValueError(
                "Saving checkpoints during training currently not supported for {model}.  Please set the number of checkpoints to 1"
            )

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
        if parameter_payload["model"] not in together.finetune_model_names:
            logger.warning(
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
            param_size = model_param_count(model)
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
                                "parameters": model_param_count(model),
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

        # Send POST request to SUBMIT FINETUNE JOB
        # HTTP headers for authorization
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "Content-Type": "application/json",
            "User-Agent": together.user_agent,
        }
        try:
            response = requests.post(
                together.api_base_finetune, headers=headers, json=parameter_payload
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def list(self) -> Dict[Any, Any]:
        verify_api_key(logger)
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.get(together.api_base_finetune, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def retrieve(self, fine_tune_id: str) -> Dict[Any, Any]:
        retrieve_url = urllib.parse.urljoin(together.api_base_finetune, fine_tune_id)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def cancel(self, fine_tune_id: str) -> Dict[Any, Any]:
        relative_path = posixpath.join(fine_tune_id, "cancel")
        retrieve_url = urllib.parse.urljoin(together.api_base_finetune, relative_path)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.post(retrieve_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

    @classmethod
    def list_events(self, fine_tune_id: str) -> Dict[Any, Any]:
        # TODO enable stream
        relative_path = posixpath.join(fine_tune_id, "events")
        retrieve_url = urllib.parse.urljoin(together.api_base_finetune, relative_path)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.get(retrieve_url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        try:
            response_json = dict(response.json())
        except Exception as e:
            logger.critical(
                f"JSON Error raised: {e}\nResponse status code = {response.status_code}"
            )
            raise together.JSONError(e, http_status=response.status_code)

        return response_json

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

        logger.info(f"Downloading weights from {model_file_path}...")

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        try:
            session = requests.Session()

            response = session.get(model_file_path, headers=headers, stream=True)
            response.raise_for_status()

            if output is None:
                content_type = str(response.headers.get("content-type"))

                output = self.retrieve(fine_tune_id)["model_output_path"].split("/")[-1]

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
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        return output  # this should be null

    # def delete_finetune_model(self, model: str) -> Dict[Any, Any]:
    #     model_url = "https://api.together.xyz/api/models"
    #     delete_url = urllib.parse.urljoin(model_url, model)

    #     headers = {
    #         "Authorization": f"Bearer {together.api_key}",
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
