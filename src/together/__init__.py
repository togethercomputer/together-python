import os
import urllib.parse
from contextvars import ContextVar
from typing import TYPE_CHECKING, Callable, Optional, Type, Union
import typing as _t
from typing_extensions import override

from together.version import VERSION

from together.together_response import TogetherResponse

version = VERSION

user_agent = f"TogetherPythonOfficial/{version}"

api_key = os.environ.get("TOGETHER_API_KEY", None)

api_base = "https://api.together.xyz/v1"
api_base_complete = urllib.parse.urljoin(api_base, "/api/inference")
api_base_files = urllib.parse.urljoin(api_base, "/v1/files/")
api_base_finetune = urllib.parse.urljoin(api_base, "/v1/fine-tunes/")
api_base_instances = urllib.parse.urljoin(api_base, "instances/")
api_base_embeddings = urllib.parse.urljoin(api_base, "api/v1/embeddings")

default_text_model = "togethercomputer/RedPajama-INCITE-7B-Chat"
default_image_model = "runwayml/stable-diffusion-v1-5"
default_embedding_model = "togethercomputer/bert-base-uncased"
log_level = "WARNING"

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

from together._constants import TIMEOUT_SECS, MAX_CONNECTION_RETRIES
from together._client import Together

import httpx as _httpx

api_key: str | None = None

organization: str | None = None

base_url: str | _httpx.URL | None = None

timeout: float | None = TIMEOUT_SECS

max_retries: int = MAX_CONNECTION_RETRIES

default_headers: _t.Mapping[str, str] | None = None

default_query: _t.Mapping[str, object] | None = None


class _ModuleClient(Together):
    # Note: we have to use type: ignores here as overriding class members
    # with properties is technically unsafe but it is fine for our use case

    @property  # type: ignore
    @override
    def api_key(self) -> str | None:
        return api_key

    @api_key.setter  # type: ignore
    def api_key(self, value: str | None) -> None:  # type: ignore
        global api_key

        api_key = value

    @property  # type: ignore
    @override
    def organization(self) -> str | None:
        return organization

    @organization.setter  # type: ignore
    def organization(self, value: str | None) -> None:  # type: ignore
        global organization

        organization = value

    @property
    @override
    def base_url(self) -> str:
        if base_url is not None:
            return base_url

        return super().base_url

    @base_url.setter
    def base_url(self, url: _httpx.URL | str) -> None:
        super().base_url = url  # type: ignore[misc]

    @property  # type: ignore
    @override
    def timeout(self) -> float | None:
        return timeout

    @timeout.setter  # type: ignore
    def timeout(self, value: float | None) -> None:  # type: ignore
        global timeout

        timeout = value

    @property  # type: ignore
    @override
    def max_retries(self) -> int:
        return max_retries

    @max_retries.setter  # type: ignore
    def max_retries(self, value: int) -> None:  # type: ignore
        global max_retries

        max_retries = value

    @property  # type: ignore
    @override
    def _custom_headers(self) -> _t.Mapping[str, str] | None:
        return default_headers

    @_custom_headers.setter  # type: ignore
    def _custom_headers(self, value: _t.Mapping[str, str] | None) -> None:  # type: ignore
        global default_headers

        default_headers = value


__all__ = [
    "aiosession",
    "api_key",
    "api_base",
    "api_base_complete",
    "api_base_files",
    "api_base_finetune",
    "api_base_instances",
    "api_base_embeddings",
    "default_text_model",
    "default_image_model",
    "default_embedding_model",
    # "Models",
    # "Complete",
    # "Completion",
    # "AsyncComplete",
    # "Files",
    # "Finetune",
    # "Image",
    # "Embeddings",
    "version",
    "MAX_CONNECTION_RETRIES",
    "MISSING_API_KEY_MESSAGE",
    "BACKOFF_FACTOR",
    "min_samples",
    "Together",
]
