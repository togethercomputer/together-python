import json
import os
import posixpath
import urllib.parse
import warnings
from typing import Any, Dict, List, Mapping, Optional, Union

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

import together
from together import error
from together.engine import Requestor
from together.utils import check_status, response_to_dict


# the number of bytes in a gigabyte, used to convert bytes to GB for readable comparison
NUM_BYTES_IN_GB = 2**30

# maximum number of GB sized files we support finetuning for
MAX_FT_GB = 4.9


class Files:
    @classmethod
    def list(self) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        # send request
        requestor = Requestor()
        response = requestor.request(method="get", path=together.api_files_path)
        response_json = response_to_dict(response)
        if response.status_code != 200:
            raise error.parse_error(response.status_code, response_json)
        return response_json

    @classmethod
    def check(self, file: str) -> Dict[str, object]:
        return check_json(file)

    @classmethod
    def upload(
        self,
        file: str,
        check: bool = True,
        model: Optional[str] = None,
    ) -> Mapping[str, Union[str, int, Any]]:
        requestor = Requestor()
        data = {"purpose": "fine-tune", "file_name": os.path.basename(file)}

        if check:
            report_dict = check_json(file)
            if not report_dict["is_check_passed"]:
                raise error.ValidationError(
                    f"Invalid file supplied. Failed to upload.\nReport:\n {report_dict}"
                )
        else:
            report_dict = {}

        try:
            response = requestor.request(
                method="post",
                path=together.api_files_path[:-1],
                data=data,
                allow_redirects=False,
                override_content_type=True,
            )

            if response.status_code != 302:
                print(response.text)
                raise error.parse_error(status_code=response.status_code)

            # Get info from headers and file
            r2_signed_url = response.headers["Location"]
            file_id = response.headers["X-Together-File-Id"]
            file_size = os.stat(file).st_size

            # Progress bar
            progress_bar = tqdm(
                total=file_size, unit="B", unit_scale=True, unit_divisor=1024
            )
            progress_bar.set_description(f"Uploading {file}")

            with open(file, "rb") as f:
                wrapped_file = CallbackIOWrapper(progress_bar.update, f, "read")
                response = requestor.request(method="put", url=r2_signed_url, data=wrapped_file, override_content_type=True, disable_headers=True)
                response.raise_for_status()

            preprocess_url = together.api_files_path + f"{file_id}/preprocess"

            response = requestor.request(
                method="post",
                path=preprocess_url,
            )

        except Exception as e:
            raise error.ResponseError(e)

        return {
            "filename": os.path.basename(file),
            "id": str(file_id),
            "object": "file",
            "report_dict": report_dict,
        }

    @classmethod
    def delete(self, file_id: str) -> Dict[str, str]:
        delete_url = together.api_files_path + file_id

        requestor = Requestor()

        response = requestor.request(method="delete", path=delete_url)
        response_json = response_to_dict(response)
        check_status(response=response)

        return response_json

    @classmethod
    def retrieve(self, file_id: str) -> Dict[str, Union[str, int]]:
        retrieve_url = together.api_files_path + file_id

        requestor = Requestor()
        response = requestor.request(method="get", path=retrieve_url)

        response_json = response_to_dict(response)
        check_status(response=response, response_json=response_json)

        return response_json

    @classmethod
    def retrieve_content(self, file_id: str, output: Union[str, None] = None) -> str:
        if output is None:
            output = file_id + ".jsonl"

        relative_path = posixpath.join(file_id, "content")
        retrieve_url = together.api_files_path + relative_path

        requestor = Requestor()
        response = requestor.request(method="get", path=retrieve_url, stream=True)
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
            warnings.warn(
                f"Caution: Downloaded file size ({progress_bar.n}) does not match remote file size ({total_size_in_bytes})."
            )

        return output

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
) -> Dict[str, object]:
    report_dict = {
        "is_check_passed": True,
        "model_special_tokens": "we are not yet checking end of sentence tokens for this model",
    }

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

    return report_dict
