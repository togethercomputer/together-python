import json
import logging
import os
import platform
import re
import sys
from datetime import datetime
from typing import Any, Dict, Optional

import requests
import sseclient

import together


logger = logging.getLogger("together")

TOGETHER_LOG = os.environ.get("TOGETHER_LOG")


def verify_api_key() -> None:
    if together.api_key is None:
        raise together.AuthenticationError(together.MISSING_API_KEY_MESSAGE)


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


def response_status_exception(response: requests.Response) -> None:
    if response.status_code == 429:
        raise together.RateLimitError(
            message="Too many requests received. Please pace your requests."
        )
    elif response.status_code == 500:
        raise Exception("server encountered an unexpected condition")
    elif response.status_code == 401:
        raise Exception("invalid authentication credentials")
    response.raise_for_status()


def format_app_info(info):
    str = info["name"]
    if info["version"]:
        str += "/%s" % (info["version"],)
    if info["url"]:
        str += " (%s)" % (info["url"],)
    return str


def get_headers(method: str, api_key: str, extra) -> Dict[str, str]:
    user_agent = "Together/v1 PythonBindings/%s" % (together.VERSION,)

    uname_without_node = " ".join(
        v for k, v in platform.uname()._asdict().items() if k != "node"
    )
    ua = {
        "bindings_version": together.VERSION,
        "httplib": "requests",
        "lang": "python",
        "lang_version": platform.python_version(),
        "platform": platform.platform(),
        "publisher": "openai",
        "uname": uname_without_node,
    }

    headers = {
        "X-TogetherAI-Client-User-Agent": json.dumps(ua),
        "Authorization": f"Bearer {api_key or together.api_key}",
        "User-Agent": user_agent,
    }

    if _console_log_level():
        headers["OpenAI-Debug"] = _console_log_level()
    headers.update(extra)

    return headers


def create_post_request(
    url: str,
    headers: Optional[Dict[Any, Any]] = None,
    json: Optional[Dict[Any, Any]] = None,
    stream: Optional[bool] = False,
    check_auth: Optional[bool] = True,
    api_key: Optional[str] = None,
) -> requests.Response:
    if check_auth and api_key is None:
        verify_api_key()

    if not headers:
        headers = get_headers()

    # send request
    try:
        response = requests.post(url, headers=headers, json=json, stream=stream)
    except requests.exceptions.RequestException as e:
        raise together.ResponseError(e)

    response_status_exception(response)

    return response


def sse_client(response: requests.Response) -> sseclient.SSEClient:
    return sseclient.SSEClient(response)  # type: ignore


def create_get_request(
    url: str,
    headers: Optional[Dict[Any, Any]] = None,
    json: Optional[Dict[Any, Any]] = None,
    stream: Optional[bool] = False,
    check_auth: Optional[bool] = True,
) -> requests.Response:
    if check_auth:
        verify_api_key()

    if not headers:
        headers = get_headers()

    # send request
    try:
        response = requests.get(url, headers=headers, json=json, stream=stream)
    except requests.exceptions.RequestException as e:
        raise together.ResponseError(e)

    response_status_exception(response)

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


def bytes_to_human_readable(num: float, suffix: Optional[str] = "B") -> str:
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def finetune_price_to_dollars(price: float) -> float:
    return price / 1000000000


def nanodollars_to_dollars(price: int) -> float:
    return (price * 4000) / 1000000000


def default_api_key(api_key: Optional[str] = None) -> str:
    if api_key:
        return api_key
    if together.api_key:
        return together.api_key
    if os.environ.get("TOGETHER_API_KEY"):
        return os.environ.get("TOGETHER_API_KEY")

    raise together.AuthenticationError(together.MISSING_API_KEY_MESSAGE)


def _console_log_level():
    if together.log in ["debug", "info"]:
        return together.log
    elif TOGETHER_LOG in ["debug", "info"]:
        return TOGETHER_LOG
    else:
        return None


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into ascii.
        if not isinstance(val, str):
            val = str(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return "{key}={val}".format(key=key, val=val)

    return " ".join([fmt(key, val) for key, val in sorted(props.items())])


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def log_warn(message, **params):
    msg = logfmt(dict(message=message, **params))
    print(msg, file=sys.stderr)
    logger.warn(msg)
