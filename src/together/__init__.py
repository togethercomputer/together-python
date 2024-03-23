from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable

from together import (
    abstract,
    client,
    constants,
    error,
    filemanager,
    resources,
    together_response,
    types,
    utils,
)
from together.version import VERSION


version = VERSION

log: str | None = None  # Set to either 'debug' or 'info', controls console logging

if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

requestssession: "requests.Session" | Callable[[], "requests.Session"] | None = None

aiosession: ContextVar["ClientSession" | None] = ContextVar(
    "aiohttp-session", default=None
)

from together.client import AsyncClient, AsyncTogether, Client, Together


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
    "filemanager",
    "error",
    "together_response",
    "client",
    "utils",
]
