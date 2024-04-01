from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

from together.constants import MAX_FILE_SIZE_GB, MIN_SAMPLES, NUM_BYTES_IN_GB


def check_file(
    file: Path | str,
) -> Dict[str, Any]:
    if not isinstance(file, Path):
        file = Path(file)

    report_dict = {
        "is_check_passed": True,
        "message": "Checks passed",
        "found": None,
        "file_size": None,
        "utf8": None,
        "line_type": None,
        "text_field": None,
        "key_value": None,
        "min_samples": None,
        "num_samples": None,
        "load_json": None,
    }

    if not file.is_file():
        report_dict["found"] = False
        report_dict["is_check_passed"] = False
        return report_dict
    else:
        report_dict["found"] = True

    file_size = os.stat(file.as_posix()).st_size

    if file_size > MAX_FILE_SIZE_GB * NUM_BYTES_IN_GB:
        report_dict["message"] = (
            f"Maximum supported file size is {MAX_FILE_SIZE_GB} GB. Found file with size of {round(file_size / NUM_BYTES_IN_GB ,3)} GB."
        )
        report_dict["is_check_passed"] = False
    elif file_size == 0:
        report_dict["message"] = "File is empty"
        report_dict["file_size"] = 0
        report_dict["is_check_passed"] = False
        return report_dict
    else:
        report_dict["file_size"] = file_size

    # Check that the file is UTF-8 encoded. If not report where the error occurs.
    try:
        with file.open(encoding="utf-8") as f:
            f.read()
        report_dict["utf8"] = True
    except UnicodeDecodeError as e:
        report_dict["utf8"] = False
        report_dict["message"] = f"File is not UTF-8 encoded. Error raised: {e}."
        report_dict["is_check_passed"] = False
        return report_dict

    with file.open() as f:
        # idx must be instantiated so decode errors (e.g. file is a tar) or empty files are caught
        idx = -1
        try:
            for idx, line in enumerate(f):
                json_line = json.loads(line)  # each line in jsonlines should be a json

                if not isinstance(json_line, dict):
                    report_dict["line_type"] = False
                    report_dict["message"] = (
                        f"Error parsing file. Invalid format on line {idx+1} of the input file. "
                        'Example of valid json: {"text": "my sample string"}. '
                    )

                    report_dict["is_check_passed"] = False

                if "text" not in json_line.keys():
                    report_dict["text_field"] = False
                    report_dict["message"] = (
                        f"Missing 'text' field was found on line {idx+1} of the the input file. "
                        "Expected format: {'text': 'my sample string'}. "
                    )
                    report_dict["is_check_passed"] = False
                else:
                    # check to make sure the value of the "text" key is a string
                    if not isinstance(json_line["text"], str):
                        report_dict["key_value"] = False
                        report_dict["message"] = (
                            f'Invalid value type for "text" key on line {idx+1}. '
                            f'Expected string. Found {type(json_line["text"])}.'
                        )

                        report_dict["is_check_passed"] = False

            # make sure this is outside the for idx, line in enumerate(f): for loop
            if idx + 1 < MIN_SAMPLES:
                report_dict["min_samples"] = False
                report_dict["message"] = (
                    f"Processing {file} resulted in only {idx+1} samples. "
                    f"Our minimum is {MIN_SAMPLES} samples. "
                )
                report_dict["is_check_passed"] = False
            else:
                report_dict["num_samples"] = idx + 1
                report_dict["min_samples"] = True

            report_dict["load_json"] = True

        except ValueError:
            report_dict["load_json"] = False
            if idx < 0:
                report_dict["message"] = (
                    "Unable to decode file. "
                    "File may be empty or in an unsupported format. "
                )
            else:
                report_dict["message"] = (
                    f"Error parsing json payload. Unexpected format on line {idx+1}."
                )
            report_dict["is_check_passed"] = False

    if report_dict["text_field"] is not False:
        report_dict["text_field"] = True
    if report_dict["line_type"] is not False:
        report_dict["line_type"] = True
    if report_dict["key_value"] is not False:
        report_dict["key_value"] = True

    return report_dict
