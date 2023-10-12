import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional, Union

import requests
import sseclient  # type: ignore

import together


class TogetherLogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%m-%d-%Y %H:%M:%S")
        return formatter.format(record)


# Setup logging
def get_logger(
    name: str,
    logger: Optional[logging.Logger] = None,
    log_level: str = together.log_level,
) -> logging.Logger:
    if logger is None:
        logger = logging.getLogger(name)

        logger.setLevel(log_level)

        lg_format = logging.StreamHandler(sys.stderr)
        lg_format.setLevel(logging.DEBUG)
        lg_format.setFormatter(TogetherLogFormatter())

        logger.addHandler(lg_format)

    return logger


def verify_api_key(logger: Optional[logging.Logger] = None) -> bool:
    if logger is None:
        logger = get_logger(str(__name__), log_level=together.log_level)
    if together.api_key is None:
        msg = (
            "TOGETHER_API_KEY not found \n"
            "Please set it as an environment variable or set it as together.api_key \n"
            "Find your TOGETHER_API_KEY at https://api.together.xyz/settings/api-keys"
        )
        print(msg)
        return False
    else:
        return True


def extract_time(json_obj: Dict[str, Any]) -> int:
    try:
        return int(json_obj["created_at"])
    except KeyError:
        return 0


def parse_timestamp(timestamp: str) -> datetime:
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt)
        except ValueError:
            continue
    raise ValueError("Timestamp does not match any expected format")


def create_post_request(
    url: str,
    headers: Optional[Dict[Any, Any]] = None,
    json: Optional[Dict[Any, Any]] = None,
    stream: Optional[bool] = False,
    check_auth: Optional[bool] = True,
) -> Union[requests.Response, None]:
    if check_auth:
        if not verify_api_key():
            return None

    if not headers:
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "Content-Type": "application/json",
            "User-Agent": together.user_agent,
        }

    # send request
    try:
        response = requests.post(url, headers=headers, json=json, stream=stream)
    except requests.exceptions.RequestException as e:
        raise together.ResponseError(e)

    if response.status_code == 429:
        raise together.InstanceError()
    elif response.status_code == 500:
        raise Exception("Invalid API key supplied.")
    response.raise_for_status()

    return response


def sse_client(response: requests.Response) -> sseclient.SSEClient:
    return sseclient.SSEClient(response)


def create_get_request(
    url: str,
    headers: Optional[Dict[Any, Any]] = None,
    json: Optional[Dict[Any, Any]] = None,
    stream: Optional[bool] = False,
    check_auth: Optional[bool] = True,
) -> Union[requests.Response, None]:
    if check_auth:
        if not verify_api_key():
            return None

    if not headers:
        headers = {
            "Authorization": f"Bearer {together.api_key}",
            "Content-Type": "application/json",
            "User-Agent": together.user_agent,
        }

    # send request
    try:
        response = requests.get(url, headers=headers, json=json, stream=stream)
    except requests.exceptions.RequestException as e:
        raise together.ResponseError(e)

    if response.status_code == 429:
        raise together.InstanceError()
    elif response.status_code == 500:
        raise Exception("Invalid API key supplied.")
    response.raise_for_status()

    return response


def response_to_dict(response: requests.Response) -> Dict[Any, Any]:
    try:
        response_json = dict(response.json())
    except Exception as e:
        raise together.JSONError(e, http_status=response.status_code)

    return response_json


def round_to_closest_multiple_of_32(batch_size: Optional[int]) -> int:
    if batch_size is None:
        return 32
    batch_size = int(batch_size)
    if batch_size < 32:
        return 32
    elif batch_size > 256:
        return 256
    return 32 * ((batch_size + 31) // 32)
