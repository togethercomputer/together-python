import asyncio
import json
import sys
import threading
import time
from json import JSONDecodeError
from typing import (
    AsyncContextManager,
    AsyncGenerator,
    Dict,
    Iterator,
    Optional,
    Tuple,
    Union,
    overload, Any, Generator,
)
from urllib.parse import urlencode, urlsplit, urlunsplit

import aiohttp
import requests

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

import together
from together import error, utils
from together.together_response import TogetherResponse

from .._constants import TIMEOUT_SECS, MAX_SESSION_LIFETIME_SECS, MAX_CONNECTION_RETRIES

# Has one attribute per thread, 'session'.
_thread_context = threading.local()


def _build_api_url(url: str, query: str) -> str:
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return str(urlunsplit((scheme, netloc, path, query, fragment)))


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
            # SSE event may be valid when it contains whitespace
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


class APIRequestor:
    def __init__(
            self,
            key=None,
            api_base=None,
    ):
        self.api_base = api_base or together.api_base
        self.api_key = key or utils.default_api_key()

    @classmethod
    def format_app_info(cls, info):
        fmt_str = info["name"]
        if info["version"]:
            fmt_str += "/%s" % (info["version"],)
        if info["url"]:
            fmt_str += " (%s)" % (info["url"],)
        return fmt_str

    @overload
    def request(
            self,
            method,
            url,
            params,
            headers,
            files,
            stream: Literal[True],
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Iterator[TogetherResponse], bool, str]:
        pass

    @overload
    def request(
            self,
            method,
            url,
            params=...,
            headers=...,
            files=...,
            *,
            stream: Literal[True],
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Iterator[TogetherResponse], bool, str]:
        pass

    @overload
    def request(
            self,
            method,
            url,
            params=...,
            headers=...,
            files=...,
            stream: Literal[False] = ...,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[TogetherResponse, bool, str]:
        pass

    @overload
    def request(
            self,
            method,
            url,
            params=...,
            headers=...,
            files=...,
            stream: bool = ...,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Union[TogetherResponse, Iterator[TogetherResponse]], bool, str]:
        pass

    def request(
            self,
            method,
            url,
            params=None,
            headers=None,
            files=None,
            stream: bool = False,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> Tuple[Union[TogetherResponse, Iterator[TogetherResponse]], bool, str]:
        result = self.request_raw(
            method.lower(),
            url,
            params=params,
            supplied_headers=headers,
            files=files,
            stream=stream,
            request_timeout=request_timeout,
        )
        resp, got_stream = self._interpret_response(result, stream)
        return resp, got_stream, self.api_key

    @overload
    async def arequest(
            self,
            method,
            url,
            params,
            headers,
            files,
            stream: Literal[True],
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[AsyncGenerator[TogetherResponse, None], bool, str]:
        pass

    @overload
    async def arequest(
            self,
            method,
            url,
            params=...,
            headers=...,
            files=...,
            *,
            stream: Literal[True],
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[AsyncGenerator[TogetherResponse, None], bool, str]:
        pass

    @overload
    async def arequest(
            self,
            method,
            url,
            params=...,
            headers=...,
            files=...,
            stream: Literal[False] = ...,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[TogetherResponse, bool, str]:
        pass

    @overload
    async def arequest(
            self,
            method,
            url,
            params=...,
            headers=...,
            files=...,
            stream: bool = ...,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    ) -> Tuple[Union[TogetherResponse, AsyncGenerator[TogetherResponse, None]], bool, str]:
        pass

    async def arequest(
            self,
            method,
            url,
            params=None,
            headers=None,
            files=None,
            stream: bool = False,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> Tuple[Union[TogetherResponse, AsyncGenerator[TogetherResponse, None]], bool, str]:
        ctx = AioHTTPSession()
        session = await ctx.__aenter__()
        result = None
        try:
            result = await self.arequest_raw(
                method.lower(),
                url,
                session,
                params=params,
                supplied_headers=headers,
                files=files,
                request_timeout=request_timeout,
            )
            resp, got_stream = await self._interpret_async_response(result, stream)
        except Exception:
            # Close the request before exiting session context.
            if result is not None:
                result.release()
            await ctx.__aexit__(None, None, None)
            raise
        if got_stream:

            async def wrap_resp():
                assert isinstance(resp, AsyncGenerator)
                try:
                    async for r in resp:
                        yield r
                finally:
                    # Close the request before exiting session context. Important to do it here
                    # as if stream is not fully exhausted, we need to close the request nevertheless.
                    result.release()
                    await ctx.__aexit__(None, None, None)

            return wrap_resp(), got_stream, self.api_key
        else:
            # Close the request before exiting session context.
            result.release()
            await ctx.__aexit__(None, None, None)
            return resp, got_stream, self.api_key

    @classmethod
    def handle_error_response(cls, rbody, rcode, resp, rheaders, stream_error=False):
        try:
            error_data = resp["error"]
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                http_body=rbody,
                http_status=rcode,
                response=resp,
            )

        utils.log_info(
            "Together API error received",
            error_code=error_data.get("code"),
            error_type=error_data.get("error_type"),
            error_message=error_data.get("error"),
            error_param=error_data.get("param"),
            stream_error=stream_error,
        )

        # Rate limits were previously coded as 400's with code 'rate_limit'
        if rcode == 429:
            return error.RateLimitError(
                error_data.get("error"),
                http_body=rbody,
                http_status=rcode,
                response=resp,
                headers=rheaders
            )
        elif rcode in [400, 404, 415]:
            return error.InvalidRequestError(
                error_data.get("error"),
                http_body=rbody,
                http_status=rcode,
                response=resp,
                headers=rheaders
            )
        elif rcode == 401:
            return error.AuthenticationError(
                error_data.get("error"),
                http_body=rbody,
                http_status=rcode,
                response=resp,
                headers=rheaders
            )

        elif stream_error:
            parts = [error_data.get("error"), "(Error occurred while streaming.)"]
            message = " ".join([p for p in parts if p is not None])
            return error.APIError(message,
                                  http_body=rbody,
                                  http_status=rcode,
                                  response=resp,
                                  headers=rheaders)
        else:
            return error.APIError(
                f"{error_data.get('error')} {rbody} {rcode} {resp} {rheaders}",
                http_body=rbody,
                http_status=rcode,
                response=resp,
                headers=rheaders
            )

    @classmethod
    def _validate_headers(
            cls, supplied_headers: Optional[Dict[str, str]]
    ) -> Dict[str, str]:
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

        # NOTE: It is possible to do more validation of the headers, but a request could always
        # be made to the API manually with invalid headers, so we need to handle them server side.

        return headers

    def _prepare_request_raw(
            self,
            url,
            supplied_headers,
            method,
            params,
            files,
    ) -> Tuple[str, Dict[str, str], Optional[bytes]]:
        abs_url = "%s%s" % (self.api_base, url)
        headers = self._validate_headers(supplied_headers)

        data = None
        if method == "get" or method == "delete":
            if params:
                encoded_params = urlencode(
                    [(k, v) for k, v in params.items() if v is not None]
                )
                abs_url = _build_api_url(abs_url, encoded_params)
        elif method in {"post", "put"}:
            if params and files:
                data = params
            if params and not files:
                data = json.dumps(params).encode()
                headers["Content-Type"] = "application/json"
        else:
            raise error.APIConnectionError(
                "Unrecognized HTTP method %r. This may indicate a bug in the "
                "Together bindings. Please contact us by filling out https://www.together.ai/contact for "
                "assistance." % (method,)
            )

        headers = utils.get_headers(method, self.api_key, headers)

        utils.log_debug("Request to Together API", method=method, path=abs_url)
        utils.log_debug("Post details", data=data)

        return abs_url, headers, data

    def request_raw(
            self,
            method,
            url,
            *,
            params=None,
            supplied_headers: Optional[Dict[str, str]] = None,
            files=None,
            stream: bool = False,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> requests.Response:
        abs_url, headers, data = self._prepare_request_raw(
            url, supplied_headers, method, params, files
        )

        print(abs_url, headers, data)

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
                files=files,
                stream=stream,
                timeout=request_timeout if request_timeout else TIMEOUT_SECS,
                proxies=_thread_context.session.proxies,
            )
        except requests.exceptions.Timeout as e:
            raise error.Timeout("Request timed out: {}".format(e)) from e
        except requests.exceptions.RequestException as e:
            raise error.APIConnectionError(
                "Error communicating with Together: {}".format(e)
            ) from e
        utils.log_debug(
            "Together API response",
            path=abs_url,
            response_code=result.status_code,
            processing_ms=result.headers.get("x-total-time"),
            request_id=result.headers.get("CF-RAY"),
        )
        # Don't read the whole stream for debug logging unless necessary.
        if together.log == "debug":
            utils.log_debug(
                "API response body", body=result.content, headers=result.headers
            )
        return result

    async def arequest_raw(
            self,
            method,
            url,
            session,
            *,
            params=None,
            supplied_headers: Optional[Dict[str, str]] = None,
            files=None,
            request_timeout: Optional[Union[float, Tuple[float, float]]] = None,
    ) -> aiohttp.ClientResponse:
        abs_url, headers, data = self._prepare_request_raw(
            url, supplied_headers, method, params, files
        )

        if isinstance(request_timeout, tuple):
            timeout = aiohttp.ClientTimeout(
                connect=request_timeout[0],
                total=request_timeout[1],
            )
        else:
            timeout = aiohttp.ClientTimeout(
                total=request_timeout if request_timeout else TIMEOUT_SECS
            )

        if files:
            # TODO: Use `aiohttp.MultipartWriter` to create the multipart form data here.
            # For now we use the private `requests` method that is known to have worked so far.
            data, content_type = requests.models.RequestEncodingMixin._encode_files(  # type: ignore
                files, data
            )
            headers["Content-Type"] = content_type
        request_kwargs = {
            "method": method,
            "url": abs_url,
            "headers": headers,
            "data": data,
            "timeout": timeout,
        }
        try:
            result = await session.request(**request_kwargs)
            utils.log_info(
                "Together API response",
                path=abs_url,
                response_code=result.status,
                processing_ms=result.headers.get("x-total-time"),
                request_id=result.headers.get("CF-RAY"),
            )
            # Don't read the whole stream for debug logging unless necessary.
            if together.log == "debug":
                utils.log_debug(
                    "API response body", body=result.content, headers=result.headers
                )
            return result
        except (aiohttp.ServerTimeoutError, asyncio.TimeoutError) as e:
            raise error.Timeout("Request timed out") from e
        except aiohttp.ClientError as e:
            raise error.APIConnectionError("Error communicating with Together") from e

    def _interpret_response(
            self, result: requests.Response, stream: bool
    ) -> Tuple[Union[TogetherResponse, Iterator[TogetherResponse]], bool]:
        """Returns the response(s) and a bool indicating whether it is a stream."""
        if stream and "text/event-stream" in result.headers.get("Content-Type", ""):
            return (
                self._interpret_response_line(
                    line, result.status_code, result.headers, stream=True
                )
                for line in parse_stream(result.iter_lines())
            ), True
        else:
            return (
                self._interpret_response_line(
                    result.content.decode("utf-8"),
                    result.status_code,
                    result.headers,
                    stream=False,
                ),
                False,
            )

    async def _interpret_async_response(
            self, result: aiohttp.ClientResponse, stream: bool
    ) -> tuple[Generator[TogetherResponse, Any, None], bool] | tuple[TogetherResponse, bool]:
        """Returns the response(s) and a bool indicating whether it is a stream."""
        if stream and "text/event-stream" in result.headers.get("Content-Type", ""):
            return (
                self._interpret_response_line(
                    line, result.status, result.headers, stream=True
                )
                async for line in parse_stream_async(result.content)
            ), True
        else:
            try:
                await result.read()
            except (aiohttp.ServerTimeoutError, asyncio.TimeoutError) as e:
                raise error.Timeout("Request timed out") from e
            except aiohttp.ClientError as e:
                utils.log_warn(e, body=result.content)
            return (
                self._interpret_response_line(
                    (await result.read()).decode("utf-8"),
                    result.status,
                    result.headers,
                    stream=False,
                ),
                False,
            )

    def _interpret_response_line(
            self, rbody: str, rcode: int, rheaders, stream: bool
    ) -> TogetherResponse:
        # HTTP 204 response code does not have any content in the body.
        if rcode == 204:
            return TogetherResponse(None, rheaders)

        if rcode == 503:
            raise error.ServiceUnavailableError(
                "The server is overloaded or not ready yet.",
                http_body=rbody,
                http_status=rcode,
                headers=rheaders,
            )
        try:
            if 'text/plain' in rheaders.get('Content-Type', ''):
                data = rbody
            else:
                data = json.loads(rbody)
        except (JSONDecodeError, UnicodeDecodeError) as e:
            raise error.APIError(
                f"HTTP code {rcode} from API ({rbody})",
                http_body=rbody,
                http_status=rcode,
                headers=rheaders
            ) from e
        resp = TogetherResponse(data, rheaders)
        # In the future, we might add a "status" parameter to errors
        # to better handle the "error while streaming" case.
        stream_error = stream and "error" in resp.data
        if stream_error or not 200 <= rcode < 300:
            raise self.handle_error_response(
                rbody, rcode, resp.data, rheaders, stream_error=stream_error
            )
        return resp


class AioHTTPSession(AsyncContextManager):
    def __init__(self):
        self._session = None
        self._should_close_session = False

    async def __aenter__(self):
        self._session = together.aiosession.get()
        if self._session is None:
            self._session = await aiohttp.ClientSession().__aenter__()
            self._should_close_session = True

        return self._session

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._session is None:
            raise RuntimeError("Session is not initialized")

        if self._should_close_session:
            await self._session.__aexit__(exc_type, exc_value, traceback)
