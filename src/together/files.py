import json
import os
import posixpath
import urllib.parse
from typing import Any, Dict, List, Mapping, Optional, Union, cast

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

import together
from together.utils.utils import get_logger, verify_api_key


logger = get_logger(str(__name__), log_level=together.log_level)

# the number of bytes in a gigabyte, used to convert bytes to GB for readable comparison
NUM_BYTES_IN_GB = 2**30

# maximum number of GB sized files we support finetuning for
MAX_FT_GB = 4.9


class Files:
    def __init__(
        self,
    ) -> None:
        verify_api_key(logger)

    @classmethod
    def list(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.get(together.api_base_files, headers=headers)
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
    def check(self, file: str, model: Optional[str] = None) -> Dict[str, object]:
        return check_json(file, model)

    @classmethod
    def upload(
        self,
        file: str,
        check: bool = True,
        model: Optional[str] = None,
    ) -> Mapping[str, Union[str, int, Any]]:
        data = {"purpose": "fine-tune", "file_name": os.path.basename(file)}

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        if check:
            report_dict = check_json(file, model)
            if not report_dict["is_check_passed"]:
                print(report_dict)
                raise together.FileTypeError("Invalid file supplied. Failed to upload.")
        else:
            report_dict = {}

        session = requests.Session()

        init_endpoint = together.api_base_files[:-1]

        logger.debug(
            f"Upload file POST request: data={data}, headers={headers}, URL={init_endpoint}, allow_redirects=False"
        )
        try:
            response = session.post(
                init_endpoint,
                data=data,
                headers=headers,
                allow_redirects=False,
            )

            logger.debug(f"Response text: {response.text}")
            logger.debug(f"Response header: {response.headers}")
            logger.debug(f"Response status code: {response.status_code}")

            if response.status_code == 401:
                logger.critical(
                    "This job would exceed your free trial credits. Please upgrade to a paid account through Settings -> Billing on api.together.ai to continue."
                )
                raise together.AuthenticationError(
                    "This job would exceed your free trial credits. Please upgrade to a paid account through Settings -> Billing on api.together.ai to continue."
                )
            elif response.status_code != 302:
                logger.critical(
                    f"Unexpected error raised by endpoint. Response status code: {response.status_code}"
                )
                raise together.ResponseError(
                    "Unexpected error raised by endpoint.",
                    http_status=response.status_code,
                )

            r2_signed_url = response.headers["Location"]
            file_id = response.headers["X-Together-File-Id"]

            logger.info(f"R2 Signed URL: {r2_signed_url}")
            logger.info("File-ID")

            logger.info("Uploading file...")

            file_size = os.stat(file).st_size
            progress_bar = tqdm(
                total=file_size, unit="B", unit_scale=True, unit_divisor=1024
            )
            progress_bar.set_description(f"Uploading {file}")
            with open(file, "rb") as f:
                wrapped_file = CallbackIOWrapper(progress_bar.update, f, "read")
                response = requests.put(r2_signed_url, data=wrapped_file)
                response.raise_for_status()

            logger.info("File uploaded.")
            logger.debug(f"status code: {response.status_code}")
            logger.info("Processing file...")
            preprocess_url = urllib.parse.urljoin(
                together.api_base_files, f"{file_id}/preprocess"
            )

            response = session.post(
                preprocess_url,
                headers=headers,
            )

            logger.info("File processed")
            logger.debug(f"Status code: {response.status_code}")

        except Exception as e:
            logger.critical(f"Response error raised: {e}")
            raise together.ResponseError(e)

        # output_dict["filename"] = os.path.basename(file)
        # output_dict["id"] = str(file_id)
        # output_dict["object"] = "file"

        return {
            "filename": os.path.basename(file),
            "id": str(file_id),
            "object": "file",
            "report_dict": report_dict,
        }

    @classmethod
    def delete(self, file_id: str) -> Dict[str, str]:
        delete_url = urllib.parse.urljoin(together.api_base_files, file_id)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            response = requests.delete(delete_url, headers=headers)
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
    def retrieve(self, file_id: str) -> Dict[str, Union[str, int]]:
        retrieve_url = urllib.parse.urljoin(together.api_base_files, file_id)

        logger.info(f"Retrieve URL: {retrieve_url}")

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
    def retrieve_content(self, file_id: str, output: Union[str, None] = None) -> str:
        if output is None:
            output = file_id + ".jsonl"

        relative_path = posixpath.join(file_id, "content")
        retrieve_url = urllib.parse.urljoin(together.api_base_files, relative_path)

        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "User-Agent": together.user_agent,
        }

        # send request
        try:
            session = requests.Session()

            response = session.get(retrieve_url, headers=headers, stream=True)
            response.raise_for_status()

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

    @classmethod
    def save_jsonl(
        self, data: Dict[str, str], output_path: str, append: bool = False
    ) -> None:
        """
        Write list of objects to a JSON lines file.
        """
        mode = "a+" if append else "w"
        with open(output_path, mode, encoding="utf-8") as f:
            for line in data:
                json_record = json.dumps(line, ensure_ascii=False)
                f.write(json_record + "\n")
        print("Wrote {} records to {}".format(len(data), output_path))

    @classmethod
    def load_jsonl(self, input_path: str) -> List[Dict[str, str]]:
        """
        Read list of objects from a JSON lines file.
        """
        data = []
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                data.append(json.loads(line.rstrip("\n|\r")))
        print("Loaded {} records from {}".format(len(data), input_path))
        return data


def check_json(
    file: str,
    model: Optional[str] = None,
) -> Dict[str, object]:
    report_dict = {
        "is_check_passed": True,
        "model_special_tokens": "we are not yet checking end of sentence tokens for this model",
    }
    num_samples_w_eos_token = 0

    model_info_dict = cast(Dict[str, Any], together.model_info_dict)

    eos_token = None
    if model is not None and model in model_info_dict:
        if "eos_token" in model_info_dict[model]:
            eos_token = model_info_dict[model]["eos_token"]
            report_dict[
                "model_special_tokens"
            ] = f"the end of sentence token for this model is {eos_token}"

    if not os.path.isfile(file):
        report_dict["file_present"] = f"File not found at given file path {file}"
        report_dict["is_check_passed"] = False
    else:
        report_dict["file_present"] = "File found"

    file_size = os.stat(file).st_size

    if file_size > MAX_FT_GB * NUM_BYTES_IN_GB:
        report_dict[
            "file_size"
        ] = f"File size {round(file_size / NUM_BYTES_IN_GB ,3)} GB is greater than our limit of 4.9 GB"
        report_dict["is_check_passed"] = False
    else:
        report_dict["file_size"] = f"File size {round(file_size / (2**30) ,3)} GB"

    with open(file) as f:
        try:
            for idx, line in enumerate(f):
                json_line = json.loads(line)  # each line in jsonlines should be a json

                if not isinstance(json_line, dict):
                    report_dict["line_type"] = (
                        "Valid json not found in one or more lines in JSONL file."
                        'Example of valid json: {"text":"my sample string"}.'
                        "see https://docs.together.ai/docs/fine-tuning."
                        f"The first line where this occur is line {idx+1}, where 1 is the first line."
                        f"{str(line)}"
                    )
                    report_dict["is_check_passed"] = False

                if "text" not in json_line:
                    report_dict["text_field"] = (
                        f'No "text" field was found on line {idx+1} of the the input file.'
                        'Expected format: {"text":"my sample string"}.'
                        "see https://docs.together.ai/docs/fine-tuning for more information."
                        f"{str(line)}"
                    )
                    report_dict["is_check_passed"] = False
                else:
                    # check to make sure the value of the "text" key is a string
                    if not isinstance(json_line["text"], str):
                        report_dict["key_value"] = (
                            f'Unexpected, value type for "text" key on line {idx+1} of the input file.'
                            'The value type of the "text" key must be a string.'
                            'Expected format: {"text":"my sample string"}'
                            "See https://docs.together.ai/docs/fine-tuning for more information."
                            f"{str(line)}"
                        )

                        report_dict["is_check_passed"] = False

                    elif eos_token:
                        if eos_token in json_line["text"]:
                            num_samples_w_eos_token += 1

            # make sure this is outside the for idx, line in enumerate(f): for loop
            if idx + 1 < together.min_samples:
                report_dict["min_samples"] = (
                    f"Processing {file} resulted in only {idx+1} samples. "
                    f"Our minimum is {together.min_samples} samples. "
                )
                report_dict["is_check_passed"] = False
            else:
                report_dict["num_samples"] = idx + 1

        except ValueError:
            report_dict["load_json"] = (
                f"File should be a valid jsonlines (.jsonl) with a json in each line."
                'Example of valid json: {"text":"my sample string"}'
                "Valid json not found in one or more lines in file."
                "see https://docs.together.ai/docs/fine-tuning."
                f"The first line where this occur is line {idx+1}, where 1 is the first line."
                f"{str(line)}"
            )
            report_dict["is_check_passed"] = False

    report_dict["num_samples_w_eos_token"] = num_samples_w_eos_token

    return report_dict
