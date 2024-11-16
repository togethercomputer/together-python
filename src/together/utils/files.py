from __future__ import annotations

import json
import os
from pathlib import Path
from traceback import format_exc
from typing import Any, Dict

from pyarrow import ArrowInvalid, parquet

from together.constants import (
    MAX_FILE_SIZE_GB,
    MIN_SAMPLES,
    NUM_BYTES_IN_GB,
    PARQUET_EXPECTED_COLUMNS,
    JSONL_REQUIRED_COLUMNS_MAP,
    REQUIRED_COLUMNS_MESSAGE,
    POSSIBLE_ROLES_CONVERSATION,
    DatasetFormat,
)


class InvalidFileFormatError(ValueError):
    """Exception raised for invalid file formats during file checks."""

    def __init__(
        self,
        message: str = "",
        line_number: int | None = None,
        error_source: str | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.line_number = line_number
        self.error_source = error_source


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
        "has_min_samples": None,
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

    data_report_dict = {}
    if file.suffix == ".jsonl":
        report_dict["filetype"] = "jsonl"
        data_report_dict = _check_jsonl(file)
    elif file.suffix == ".parquet":
        report_dict["filetype"] = "parquet"
        data_report_dict = _check_parquet(file)
    else:
        report_dict["filetype"] = (
            f"Unknown extension of file {file}. "
            "Only files with extensions .jsonl and .parquet are supported."
        )
        report_dict["is_check_passed"] = False

    report_dict.update(data_report_dict)

    return report_dict


def _check_jsonl(file: Path) -> Dict[str, Any]:
    report_dict: Dict[str, Any] = {}
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

    dataset_format = None
    with file.open() as f:
        idx = -1
        try:
            for idx, line in enumerate(f):
                json_line = json.loads(line)

                if not isinstance(json_line, dict):
                    raise InvalidFileFormatError(
                        message=(
                            f"Error parsing file. Invalid format on line {idx + 1} of the input file. "
                            'Example of valid json: {"text": "my sample string"}. '
                        ),
                        line_number=idx + 1,
                        error_source="line_type",
                    )

                current_format = None
                for possible_format in JSONL_REQUIRED_COLUMNS_MAP:
                    if all(
                        column in json_line
                        for column in JSONL_REQUIRED_COLUMNS_MAP[possible_format]
                    ):
                        if current_format is None:
                            current_format = possible_format
                        elif current_format != possible_format:
                            raise InvalidFileFormatError(
                                message="Found multiple dataset formats in the input file. "
                                f"Got {current_format} and {possible_format} on line {idx + 1}.",
                                line_number=idx + 1,
                                error_source="format",
                            )

                if current_format is None:
                    raise InvalidFileFormatError(
                        message=(
                            f"Error parsing file. Could not detect a format for the line {idx + 1} with the columns:\n"
                            f"{json_line.keys()}"
                        ),
                        line_number=idx + 1,
                        error_source="format",
                    )

                if current_format == DatasetFormat.CONVERSATION:
                    message_column = JSONL_REQUIRED_COLUMNS_MAP[
                        DatasetFormat.CONVERSATION
                    ][0]
                    if not isinstance(json_line[message_column], list):
                        raise InvalidFileFormatError(
                            message=f"Invalid format on line {idx + 1} of the input file. "
                            f"Expected a list of messages. Found {type(json_line[message_column])}",
                            line_number=idx + 1,
                            error_source="key_value",
                        )

                    for turn_id, turn in enumerate(json_line[message_column]):
                        if not isinstance(turn, dict):
                            raise InvalidFileFormatError(
                                message=f"Invalid format on line {idx + 1} of the input file. "
                                f"Expected a dictionary in the {turn_id + 1} turn. Found {type(turn)}",
                                line_number=idx + 1,
                                error_source="key_value",
                            )

                    previous_role = None
                    for turn in json_line[message_column]:
                        for column in REQUIRED_COLUMNS_MESSAGE:
                            if column not in turn:
                                raise InvalidFileFormatError(
                                    message=f"Field `{column}` is missing for a turn `{turn}` on line {idx + 1} "
                                    "of the the input file.",
                                    line_number=idx + 1,
                                    error_source="key_value",
                                )
                            else:
                                if not isinstance(turn[column], str):
                                    raise InvalidFileFormatError(
                                        message=f"Invalid format on line {idx + 1} in the column {column} for turn `{turn}` "
                                        f"of the input file. Expected string. Found {type(turn[column])}",
                                        line_number=idx + 1,
                                        error_source="text_field",
                                    )
                        role = turn["role"]

                        if role not in POSSIBLE_ROLES_CONVERSATION:
                            raise InvalidFileFormatError(
                                message=f"Found invalid role `{role}` in the messages on the line {idx + 1}. "
                                f"Possible roles in the conversation are: {POSSIBLE_ROLES_CONVERSATION}",
                                line_number=idx + 1,
                                error_source="key_value",
                            )

                        if previous_role == role:
                            raise InvalidFileFormatError(
                                message=f"Invalid role turns on line {idx + 1} of the input file. "
                                "`user` and `assistant` roles must alternate user/assistant/user/assistant/...",
                                line_number=idx + 1,
                                error_source="key_value",
                            )

                        previous_role = role

                else:
                    for column in JSONL_REQUIRED_COLUMNS_MAP[current_format]:
                        if not isinstance(json_line[column], str):
                            raise InvalidFileFormatError(
                                message=f'Invalid value type for "{column}" key on line {idx + 1}. '
                                f"Expected string. Found {type(json_line[column])}.",
                                line_number=idx + 1,
                                error_source="key_value",
                            )

                if dataset_format is None:
                    dataset_format = current_format
                elif current_format is not None:
                    if current_format != dataset_format:
                        raise InvalidFileFormatError(
                            message="All samples in the dataset must have the same dataset format. "
                            f"Got {dataset_format} for the first line and {current_format} "
                            f"for the line {idx + 1}.",
                            line_number=idx + 1,
                            error_source="format",
                        )

            if idx + 1 < MIN_SAMPLES:
                report_dict["has_min_samples"] = False
                report_dict["message"] = (
                    f"Processing {file} resulted in only {idx + 1} samples. "
                    f"Our minimum is {MIN_SAMPLES} samples. "
                )
                report_dict["is_check_passed"] = False
            else:
                report_dict["num_samples"] = idx + 1
                report_dict["has_min_samples"] = True
                report_dict["is_check_passed"] = True

            report_dict["load_json"] = True

        except InvalidFileFormatError as e:
            report_dict["load_json"] = False
            report_dict["is_check_passed"] = False
            report_dict["message"] = e.message
            if e.line_number is not None:
                report_dict["line_number"] = e.line_number
            if e.error_source is not None:
                report_dict[e.error_source] = False
        except ValueError:
            report_dict["load_json"] = False
            if idx < 0:
                report_dict["message"] = (
                    "Unable to decode file. "
                    "File may be empty or in an unsupported format. "
                )
            else:
                report_dict["message"] = (
                    f"Error parsing json payload. Unexpected format on line {idx + 1}."
                )
            report_dict["is_check_passed"] = False

    if "text_field" not in report_dict:
        report_dict["text_field"] = True
    if "line_type" not in report_dict:
        report_dict["line_type"] = True
    if "key_value" not in report_dict:
        report_dict["key_value"] = True
    return report_dict


def _check_parquet(file: Path) -> Dict[str, Any]:
    report_dict: Dict[str, Any] = {}

    try:
        table = parquet.read_table(str(file), memory_map=True)
    except ArrowInvalid:
        report_dict["load_parquet"] = (
            f"An exception has occurred when loading the Parquet file {file}. Please check the file for corruption. "
            f"Exception trace:\n{format_exc()}"
        )
        report_dict["is_check_passed"] = False
        return report_dict

    column_names = table.schema.names
    if "input_ids" not in column_names:
        report_dict["load_parquet"] = (
            f"Parquet file {file} does not contain the `input_ids` column."
        )
        report_dict["is_check_passed"] = False
        return report_dict

    for column_name in column_names:
        if column_name not in PARQUET_EXPECTED_COLUMNS:
            report_dict["load_parquet"] = (
                f"Parquet file {file} contains an unexpected column {column_name}. "
                f"Only columns {PARQUET_EXPECTED_COLUMNS} are supported."
            )
            report_dict["is_check_passed"] = False
            return report_dict

    num_samples = len(table)
    if num_samples < MIN_SAMPLES:
        report_dict["has_min_samples"] = False
        report_dict["message"] = (
            f"Processing {file} resulted in only {num_samples} samples. "
            f"Our minimum is {MIN_SAMPLES} samples. "
        )
        report_dict["is_check_passed"] = False
        return report_dict
    else:
        report_dict["num_samples"] = num_samples

    report_dict["is_check_passed"] = True

    return report_dict
