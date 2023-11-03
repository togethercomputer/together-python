import logging
from datetime import datetime
from typing import Any, Dict, Optional

import requests
import sseclient  # type: ignore

import together
from together.error import JSONError, ResponseError, UnauthorizedError, parse_error


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


def verify_api_key() -> None:
    if together.api_key is None:
        raise UnauthorizedError(
            "TOGETHER_API_KEY not found. Please set it as an environment variable or set it with together.api_key"
        )


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


def get_headers() -> Dict[str, str]:
    headers = {
        "Authorization": f"Bearer {together.api_key}",
        "Content-Type": "application/json",
        "User-Agent": together.user_agent,
    }
    return headers


def sse_client(response: requests.Response) -> sseclient.SSEClient:
    return sseclient.SSEClient(response)


def response_to_dict(response: requests.Response) -> Dict[Any, Any]:
    try:
        response_json = dict(response.json())
    except Exception as e:
        raise JSONError(e, status_code=response.status_code)

    return response_json


def create_get_request(
    url: str,
    headers: Optional[dict[Any, Any]] = None,
    json: Optional[dict[Any, Any]] = None,
    stream: Optional[bool] = False,
    check_auth: Optional[bool] = True,
) -> Dict[Any, Any]:
    if check_auth:
        verify_api_key()

    headers = headers or get_headers()

    # send request
    try:
        response = requests.get(url, headers=headers, json=json, stream=stream)
    except requests.exceptions.RequestException as e:
        raise ResponseError(e)

    response_json = response_to_dict(response)
    if response.status_code != 200:
        raise parse_error(response.status_code, response_json)

    return response_json


def create_post_request(
    url: str,
    headers: Optional[dict[Any, Any]] = None,
    json: Optional[dict[Any, Any]] = None,
    stream: Optional[bool] = False,
    check_auth: Optional[bool] = True,
) -> Dict[Any, Any]:
    if check_auth:
        verify_api_key()

    headers = headers or get_headers()

    # send request
    try:
        response = requests.post(url, headers=headers, json=json, stream=stream)
    except requests.exceptions.RequestException as e:
        raise ResponseError(e)

    response_json = response_to_dict(response)
    if response.status_code != 200:
        raise parse_error(response.status_code, response_json)

    return response_json
