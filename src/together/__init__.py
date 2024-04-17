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
    import httpx

http_client: "httpx.Client" | Callable[[], "httpx.Client"] | None = None

async_http_client: "httpx.AsyncClient" | Callable[[], "httpx.AsyncClient"] | None = None

from together.client import AsyncClient, AsyncTogether, Client, Together


api_key: str | None = None  # To be deprecated in the next major release

# Legacy functions
from together.legacy.complete import AsyncComplete, Complete, Completion
from together.legacy.embeddings import Embeddings
from together.legacy.files import Files
from together.legacy.finetune import Finetune
from together.legacy.images import Image
from together.legacy.models import Models


__all__ = [
    "http_client",
    "async_http_client",
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
