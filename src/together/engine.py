import aiohttp
import platform
import json

import requests
import time
import threading
import urllib.parse

import together
from together import utils, version
from together import error

from typing import Iterator, Optional, Dict, Union, Tuple


TIMEOUT_SECS = 600
MAX_SESSION_LIFETIME_SECS = 180
MAX_CONNECTION_RETRIES = 2

_thread_context = threading.local()


def _make_session() -> requests.Session:
    if together.requestssession:
        if isinstance(together.requestssession, requests.Session):
            return together.requestssession
        return together.requestssession()
    s = requests.Session()
    s.mount(
        "https://",
        requests.adapters.HTTPAdapter(max_retries=MAX_CONNECTION_RETRIES),
    )
    return s

def parse_stream_helper(line: bytes) -> Optional[str]:
    if line and line.startswith(b"data:"):
        if line.startswith(b"data: "):
            # SSE event may be valid when it contain whitespace
            line = line[len(b"data: "):]
        else:
            line = line[len(b"data:"):]
        if line.strip() == b"[DONE]":
            # return here will cause GeneratorExit exception in urllib3
            # and it will close http connection with TCP Reset
            return None
        else:
            return line.decode("utf-8")
    return None

def parse_stream(rbody: Iterator[bytes]) -> Iterator[str]:
    for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line


async def parse_stream_async(rbody: aiohttp.StreamReader):
    async for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line

def validate_headers(supplied_headers: Optional[Dict[str, str]]):
    headers: Dict[str, str] = {}
    if supplied_headers is None:
        return headers

    if not isinstance(supplied_headers, dict):
        raise TypeError("Headers must be a dictionary")

    for k, v in supplied_headers.items():
        if not isinstance(k, str):
            raise TypeError("Header keys must be strings")
        if not isinstance(v, str):
            raise TypeError("Header values must be strings")
        headers[k] = v

    return headers

def get_headers(
        method: str,
        supplied_headers: Optional[Dict[str, str]],
        override_content_type: bool = False
    ) -> Dict[str, str]:
    headers = validate_headers(supplied_headers)

    user_agent = f"TogetherPythonOfficial/{version}"

    agent_args = {
            "library_version": version,
            "httplib": "requests",
            "lang": "python",
            "lang_version": platform.python_version(),
            "platform": platform.platform(),
            "publisher": "together",
        }

    headers["Authorization"] = f"Bearer {utils.default_api_key()}"
    headers["User-Agent"] = user_agent
    headers["X-Together-Client-User-Agent"] = json.dumps(agent_args)

    if method in ["post", "put"] and not override_content_type:
        headers["Content-Type"] = "application/json"

    return headers

class Requestor:
    def __init__(self, api_base: Optional[str] = None) -> None:
        self.api_base = api_base or together.api_base

    def request(
        self,
        method: str,
        path: str = None,
        supplied_headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, str]] = None,
        stream: bool = False,
        request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
        allow_redirects: bool = True,
        url: Optional[str] = None,
        override_content_type: bool = False,
        disable_headers: bool = False
    ) -> requests.Response:
        abs_url = url or urllib.parse.urljoin(together.api_base, path)

        if not disable_headers:
            headers = get_headers(method=method, supplied_headers=supplied_headers, override_content_type=override_content_type)
        else:
            headers = None

        if not hasattr(_thread_context, "session"):
            _thread_context.session = _make_session()
            _thread_context.session_create_time = time.time()
        elif (
            time.time() - getattr(_thread_context, "session_create_time", 0)
            >= MAX_SESSION_LIFETIME_SECS
        ):
            _thread_context.session.close()
            _thread_context.session = _make_session()
            _thread_context.session_create_time = time.time()

        try:
            result = _thread_context.session.request(
                method,
                abs_url,
                headers=headers,
                data=data,
                json=json_data,
                stream=stream,
                timeout=request_timeout if request_timeout else TIMEOUT_SECS,
                allow_redirects=allow_redirects,
            )
        except requests.exceptions.Timeout as e:
            raise error.TimeoutError(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            raise error.ConnectionError(f"Error communicating with Together: {e}")
        return result