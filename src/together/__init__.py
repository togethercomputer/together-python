from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable, Optional, Union

from together.version import VERSION
from together import constants
from together import (
    resources,
    types,
    abstract,
    downloadmanager,
    error,
    together_response,
    utils,
    client,
)


version = VERSION

log = None  # Set to either 'debug' or 'info', controls console logging

if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

requestssession: Optional[
    Union["requests.Session", Callable[[], "requests.Session"]]
] = None

aiosession: ContextVar[Optional["ClientSession"]] = ContextVar(
    "aiohttp-session", default=None
)

from together.client import AsyncTogether, Together, Client, AsyncClient


__all__ = [
    "aiosession",
    "constants",
    "version",
    "Together",
    "AsyncTogether",
    "Client",
    "AsyncClient",
    "resources",
    "types",
    "abstract",
    "downloadmanager",
    "error",
    "together_response",
    "utils",
    "client",
]
