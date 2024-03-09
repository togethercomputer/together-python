import os
import typing as _t
import urllib.parse
from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable, Optional, Type, Union

from typing_extensions import override

from together.together_response import TogetherResponse
from together.version import VERSION


version = VERSION

MISSING_API_KEY_MESSAGE = """TOGETHER_API_KEY not found.
Please set it as an environment variable or set it as together.api_key
Find your TOGETHER_API_KEY at https://api.together.xyz/settings/api-keys"""

MAX_CONNECTION_RETRIES = 2
BACKOFF_FACTOR = 0.2

log = None  # Set to either 'debug' or 'info', controls console logging

min_samples = 100

requestssession: Optional[
    Union["requests.Session", Callable[[], "requests.Session"]]
] = None


if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

aiosession: ContextVar[Optional["ClientSession"]] = ContextVar(
    "aiohttp-session", default=None
)

from together.client import AsyncTogether, Together


__all__ = ["aiosession", "version", "min_samples", "Together", "AsyncTogether"]
