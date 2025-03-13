from __future__ import annotations

import json
import os
import sys
import platform
from typing import TYPE_CHECKING, Any, Dict


if TYPE_CHECKING:
    from _typeshed import SupportsKeysAndGetItem

import together
from together import error
from together.utils._log import _console_log_level
from together.utils import log_info


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


def get_google_colab_secret(secret_name: str = "TOGETHER_API_KEY") -> str | None:
    """
    Checks to see if the user is running in Google Colab, and looks for the Together API Key secret.

    Args:
        secret_name (str, optional). Defaults to TOGETHER_API_KEY

    Returns:
        str: if the API key is found; None if an error occurred or the secret was not found.
    """
    # If running in Google Colab, check for Together in notebook secrets
    if "google.colab" in sys.modules:
        if TYPE_CHECKING:
            from google.colab import userdata  # type: ignore
        else:
            from google.colab import userdata

        try:
            api_key = userdata.get(secret_name)
            if not isinstance(api_key, str):
                return None
            else:
                return str(api_key)
        except userdata.NotebookAccessError:
            log_info(
                "The TOGETHER_API_KEY Colab secret was found, but notebook access is disabled. Please enable notebook "
                "access for the secret."
            )
        except userdata.SecretNotFoundError:
            # warn and carry on
            log_info("Colab: No Google Colab secret named TOGETHER_API_KEY was found.")

        return None

    else:
        return None
