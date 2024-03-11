from __future__ import annotations

import json
import logging
import os
import platform
import re
import sys
from typing import TYPE_CHECKING, Any, Dict


if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem

import together
from together import error


logger = logging.getLogger("together")

TOGETHER_LOG = os.environ.get("TOGETHER_LOG")


def get_headers(
    method: str | None = None,
    api_key: str | None = None,
    extra: "SupportsKeysAndGetItem[str, Any] | None" = None,
) -> Dict[str, str]:
    """
    Generates request headers with API key, metadata, and supplied headers

    Args:
        method (str, optional): HTTP request type (POST, GET, etc.)
            Defaults to None.
        api_key (str, optional): API key to add as an Authorization header.
            Defaults to None.
        extra (SupportsKeysAndGetItem[str, Any], optional): Additional headers to add to request.
            Defaults to None.

    Returns:
        headers (Dict[str, str]): Compiled headers from data
    """

    user_agent = "Together/v1 PythonBindings/%s" % (together.version,)

    uname_without_node = " ".join(
        v for k, v in platform.uname()._asdict().items() if k != "node"
    )
    ua = {
        "bindings_version": together.version,
        "httplib": "requests",
        "lang": "python",
        "lang_version": platform.python_version(),
        "platform": platform.platform(),
        "publisher": "together",
        "uname": uname_without_node,
    }

    headers: Dict[str, Any] = {
        "X-Together-Client-User-Agent": json.dumps(ua),
        "Authorization": f"Bearer {default_api_key(api_key)}",
        "User-Agent": user_agent,
    }

    if _console_log_level():
        headers["Together-Debug"] = _console_log_level()
    if extra:
        headers.update(extra)

    return headers


def default_api_key(api_key: str | None = None) -> str | None:
    """
    API key fallback logic from input argument and environment variable

    Args:
        api_key (str, optional): Supplied API key. This argument takes priority over env var

    Returns:
        together_api_key (str): Returns API key from supplied input or env var

    Raises:
        together.error.AuthenticationError: if API key not found
    """
    if api_key:
        return api_key
    if os.environ.get("TOGETHER_API_KEY"):
        return os.environ.get("TOGETHER_API_KEY")

    raise error.AuthenticationError(together.constants.MISSING_API_KEY_MESSAGE)


def _console_log_level() -> str | None:
    if together.log in ["debug", "info"]:
        return together.log
    elif TOGETHER_LOG in ["debug", "info"]:
        return TOGETHER_LOG
    else:
        return None


def logfmt(props: Dict[str, Any]) -> str:
    def fmt(key: str, val: Any) -> str:
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


def log_debug(message: str | Any, **params: Any) -> None:
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message: str | Any, **params: Any) -> None:
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def log_warn(message: str | Any, **params: Any) -> None:
    msg = logfmt(dict(message=message, **params))
    print(msg, file=sys.stderr)
    logger.warn(msg)


def enforce_trailing_slash(url: str) -> str:
    if not url.endswith("/"):
        return url + "/"
    else:
        return url


def normalize_key(key: str) -> str:
    return key.replace("/", "--").replace("_", "-").replace(" ", "-").lower()
