from __future__ import annotations

import asyncio
import email.utils
import json
import sys
import time
from json import JSONDecodeError
from random import random
from typing import Any, AsyncGenerator, AsyncIterator, Dict, Iterator, Tuple, overload
from urllib.parse import urlencode, urlsplit, urlunsplit

import httpx
from tqdm.utils import CallbackIOWrapper


if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from together import error, utils
from together.constants import (
    BASE_URL,
    INITIAL_RETRY_DELAY,
    MAX_RETRIES,
    MAX_RETRY_DELAY,
    TIMEOUT_SECS,
)
from together.together_response import TogetherResponse
from together.types import TogetherClient, TogetherRequest
from together.types.error import TogetherErrorResponse


def _build_api_url(url: str, query: str) -> str:
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return str(urlunsplit((scheme, netloc, path, query, fragment)))


def parse_stream_helper(line: str) -> str | None:
    if line and line.startswith("data:"):
        if line.startswith("data: "):
            # SSE event may be valid when it contains whitespace
            line = line[len("data: ") :]
        else:
            line = line[len("data:") :]
        if line.strip() == "[DONE]":
            # return here will cause GeneratorExit exception in urllib3
            # and it will close http connection with TCP Reset
            return None
        else:
            return line
    return None


def parse_stream(rbody: Iterator[str]) -> Iterator[str]:
    for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line


async def parse_stream_async(
    rbody: AsyncIterator[str],
) -> AsyncGenerator[str, Any]:
    async for line in rbody:
        _line = parse_stream_helper(line)
        if _line is not None:
            yield _line


class APIRequestor:
    def __init__(self, client: TogetherClient):
        self.api_base = client.base_url or BASE_URL
        self.api_key = client.api_key or utils.default_api_key()
        self.retries = MAX_RETRIES if client.max_retries is None else client.max_retries
        self.supplied_headers = client.supplied_headers
        self.timeout = client.timeout or TIMEOUT_SECS
        self.client = httpx.Client(http2=client.http2)
        self.async_client = httpx.AsyncClient(http2=client.http2)

    def _parse_retry_after_header(
        self, response_headers: Dict[str, Any] | None = None
    ) -> float | None:
        """
        Returns a float of the number of seconds (not milliseconds)
        to wait after retrying, or None if unspecified.

        About the Retry-After header:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
        See also
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After#syntax
        """
        if response_headers is None:
            return None

        # First, try the non-standard `retry-after-ms` header for milliseconds,
        # which is more precise than integer-seconds `retry-after`
        try:
            retry_ms_header = response_headers.get("retry-after-ms", None)
            return float(retry_ms_header) / 1000
        except (TypeError, ValueError):
            pass

        # Next, try parsing `retry-after` header as seconds (allowing nonstandard floats).
        retry_header = str(response_headers.get("retry-after"))
        try:
            # note: the spec indicates that this should only ever be an integer
            # but if someone sends a float there's no reason for us to not respect it
            return float(retry_header)
        except (TypeError, ValueError):
            pass

        # Last, try parsing `retry-after` as a date.
        retry_date_tuple = email.utils.parsedate_tz(retry_header)
        if retry_date_tuple is None:
            return None

        retry_date = email.utils.mktime_tz(retry_date_tuple)
        return float(retry_date - time.time())

    def _calculate_retry_timeout(
        self,
        remaining_retries: int,
        response_headers: Dict[str, Any] | None = None,
    ) -> float:
        # If the API asks us to wait a certain amount of time (and it's a reasonable amount), just do what it says.
        retry_after = self._parse_retry_after_header(response_headers)
        if retry_after is not None and 0 < retry_after <= 60:
            return retry_after

        nb_retries = self.retries - remaining_retries

        # Apply exponential backoff, but not more than the max.
        sleep_seconds = min(INITIAL_RETRY_DELAY * pow(2.0, nb_retries), MAX_RETRY_DELAY)

        # Apply some jitter, plus-or-minus half a second.
        jitter = 1 - 0.25 * random()
        timeout = sleep_seconds * jitter
        return timeout if timeout >= 0 else 0

    def _retry_request(
        self,
        options: TogetherRequest,
        remaining_retries: int,
        response_headers: Dict[str, Any] | None,
        *,
        stream: bool,
        request_timeout: float | None = None,
    ) -> httpx.Response:
        remaining = remaining_retries - 1
        if remaining == 1:
            utils.log_debug("1 retry left")
        else:
            utils.log_debug(f"{remaining} retries left")

        timeout = self._calculate_retry_timeout(remaining, response_headers)
        ("Retrying request to %s in %f seconds", options.url, timeout)

        # In a synchronous context we are blocking the entire thread. Up to the library user to run the client in a
        # different thread if necessary.
        time.sleep(timeout)

        return self.request_raw(
            options=options,
            stream=stream,
            request_timeout=request_timeout,
            remaining_retries=remaining,
        )

    async def _retry_async_request(
        self,
        options: TogetherRequest,
        remaining_retries: int,
        response_headers: Dict[str, Any] | None,
        *,
        stream: bool,
        request_timeout: float | None = None,
    ) -> httpx.Response:
        remaining = remaining_retries - 1
        if remaining == 1:
            utils.log_debug("1 retry left")
        else:
            utils.log_debug(f"{remaining} retries left")

        timeout = self._calculate_retry_timeout(remaining, response_headers)
        utils.log_debug(f"Retrying request to {options.url} in {timeout} seconds")

        await asyncio.sleep(timeout)

        return await self.arequest_raw(
            options=options,
            stream=stream,
            request_timeout=request_timeout,
            remaining_retries=remaining,
        )

    @overload
    def request(
        self,
        options: TogetherRequest,
        stream: Literal[True],
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[Iterator[TogetherResponse], bool, str | None]:
        pass

    @overload
    def request(
        self,
        options: TogetherRequest,
        stream: Literal[False] = ...,
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[TogetherResponse, bool, str | None]:
        pass

    @overload
    def request(
        self,
        options: TogetherRequest,
        stream: bool = ...,
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[TogetherResponse | Iterator[TogetherResponse], bool, str | None]:
        pass

    def request(
        self,
        options: TogetherRequest,
        stream: bool = False,
        remaining_retries: int | None = None,
        request_timeout: float | None = None,
    ) -> Tuple[
        TogetherResponse | Iterator[TogetherResponse],
        bool,
        str | None,
    ]:
        result = self.request_raw(
            options=options,
            remaining_retries=remaining_retries or self.retries,
            stream=stream,
            request_timeout=request_timeout,
        )

        resp, got_stream = self._interpret_response(result, stream)
        return resp, got_stream, self.api_key

    @overload
    async def arequest(
        self,
        options: TogetherRequest,
        stream: Literal[True],
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[AsyncGenerator[TogetherResponse, None], bool, str | None]:
        pass

    @overload
    async def arequest(
        self,
        options: TogetherRequest,
        *,
        stream: Literal[True],
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[AsyncGenerator[TogetherResponse, None], bool, str | None]:
        pass

    @overload
    async def arequest(
        self,
        options: TogetherRequest,
        stream: Literal[False] = ...,
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[TogetherResponse, bool, str]:
        pass

    @overload
    async def arequest(
        self,
        options: TogetherRequest,
        stream: bool = ...,
        remaining_retries: int | None = ...,
        request_timeout: float | None = ...,
    ) -> Tuple[
        TogetherResponse | AsyncGenerator[TogetherResponse, None], bool, str | None
    ]:
        pass

    async def arequest(
        self,
        options: TogetherRequest,
        stream: bool = False,
        remaining_retries: int | None = None,
        request_timeout: float | None = None,
    ) -> Tuple[
        TogetherResponse | AsyncGenerator[TogetherResponse, None], bool, str | None
    ]:
        result = await self.arequest_raw(
            options=options,
            remaining_retries=remaining_retries or self.retries,
            stream=stream,
            request_timeout=request_timeout,
        )

        resp, got_stream = await self._interpret_async_response(result, stream)
        return resp, got_stream, self.api_key

    @classmethod
    def handle_error_response(
        cls,
        resp: TogetherResponse,
        rcode: int,
        stream_error: bool = False,
    ) -> Exception:
        try:
            assert isinstance(resp.data, dict)
            error_resp = resp.data.get("error")
            assert isinstance(
                error_resp, dict
            ), f"Unexpected error response {error_resp}"
            error_data = TogetherErrorResponse(**(error_resp))
        except (KeyError, TypeError):
            raise error.JSONError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (resp.data, rcode),
                http_status=rcode,
            )

        utils.log_info(
            "Together API error received",
            error_code=error_data.code,
            error_type=error_data.type_,
            error_message=error_data.message,
            error_param=error_data.param,
            stream_error=stream_error,
        )

        # Rate limits were previously coded as 400's with code 'rate_limit'
        if rcode == 429:
            return error.RateLimitError(
                error_data,
                http_status=rcode,
                headers=resp._headers,
                request_id=resp.request_id,
            )
        elif rcode in [400, 403, 404, 415]:
            return error.InvalidRequestError(
                error_data,
                http_status=rcode,
                headers=resp._headers,
                request_id=resp.request_id,
            )
        elif rcode == 401:
            return error.AuthenticationError(
                error_data,
                http_status=rcode,
                headers=resp._headers,
                request_id=resp.request_id,
            )

        elif stream_error:
            parts = [error_data.message, "(Error occurred while streaming.)"]
            message = " ".join([p for p in parts if p is not None])
            return error.APIError(
                message,
                http_status=rcode,
                headers=resp._headers,
                request_id=resp.request_id,
            )
        else:
            return error.APIError(
                error_data,
                http_status=rcode,
                headers=resp._headers,
                request_id=resp.request_id,
            )

    @classmethod
    def _validate_headers(
        cls, supplied_headers: Dict[str, str] | None
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
        options: TogetherRequest,
        absolute: bool = False,
    ) -> Tuple[str, Dict[str, str], Dict[str, str] | CallbackIOWrapper | bytes | None]:
        abs_url = options.url if absolute else "%s%s" % (self.api_base, options.url)
        headers = self._validate_headers(options.headers or self.supplied_headers)

        data = None
        data_bytes = None
        if options.method.lower() == "get" or options.method.lower() == "delete":
            if options.params:
                encoded_params = urlencode(
                    [(k, v) for k, v in options.params.items() if v is not None]
                )
                abs_url = _build_api_url(abs_url, encoded_params)
        elif options.method.lower() in {"post", "put"}:
            if options.params and (options.files or options.override_headers):
                data = options.params
            elif options.params and not options.files:
                data_bytes = json.dumps(options.params).encode()
                headers["Content-Type"] = "application/json"

        else:
            raise error.APIConnectionError(
                "Unrecognized HTTP method %r. This may indicate a bug in the "
                "Together SDK. Please contact us by filling out https://www.together.ai/contact for "
                "assistance." % (options.method,)
            )

        if not options.override_headers:
            headers = utils.get_headers(options.method, self.api_key, headers)

        utils.log_debug(
            "Request to Together API",
            method=options.method,
            path=abs_url,
            post_data=(data or data_bytes),
            headers=json.dumps(headers),
        )

        return abs_url, headers, (data or data_bytes)

    def request_raw(
        self,
        options: TogetherRequest,
        remaining_retries: int,
        *,
        stream: bool = False,
        request_timeout: float | None = None,
        absolute: bool = False,
    ) -> httpx.Response:
        abs_url, headers, data = self._prepare_request_raw(options, absolute)

        try:
            req = self.client.build_request(
                options.method,
                abs_url,
                headers=headers,
                data=data,  # type: ignore
                files=options.files,
                timeout=request_timeout or self.timeout,
            )

            result = self.client.send(
                req, stream=stream, follow_redirects=options.allow_redirects
            )

        except httpx.TimeoutException as e:
            utils.log_debug("Encountered httpx.TimeoutException")

            try:
                resp_headers = dict(result.headers)
            except AttributeError:
                resp_headers = {}

            if remaining_retries > 0:
                return self._retry_request(
                    options,
                    remaining_retries=remaining_retries,
                    response_headers=resp_headers,
                    stream=stream,
                    request_timeout=request_timeout,
                )

            raise error.Timeout("Request timed out: {}".format(e)) from e
        except httpx.RequestError as e:
            utils.log_debug("Encountered httpx.RequestError")

            try:
                resp_headers = dict(result.headers)
            except AttributeError:
                resp_headers = {}

            if remaining_retries > 0:
                return self._retry_request(
                    options,
                    remaining_retries=remaining_retries,
                    response_headers=resp_headers,
                    stream=stream,
                    request_timeout=request_timeout,
                )

            raise error.APIConnectionError(
                "Error communicating with API: {}".format(e)
            ) from e

        # retry on 5XX error or rate-limit
        if 500 <= result.status_code < 600 or result.status_code == 429:
            utils.log_debug(
                f"Encountered status error. Error code: {result.status_code}"
            )

            if remaining_retries > 0:
                return self._retry_request(
                    options,
                    remaining_retries=remaining_retries,
                    response_headers=dict(result.headers),
                    stream=stream,
                    request_timeout=request_timeout,
                )

        utils.log_debug(
            "Together API response",
            path=abs_url,
            response_code=result.status_code,
            processing_ms=result.headers.get("x-total-time"),
            request_id=result.headers.get("CF-RAY"),
        )

        return result

    async def arequest_raw(
        self,
        options: TogetherRequest,
        remaining_retries: int,
        *,
        stream: bool = False,
        request_timeout: float | None = None,
        absolute: bool = False,
    ) -> httpx.Response:
        abs_url, headers, data = self._prepare_request_raw(options, absolute)

        try:
            req = self.async_client.build_request(
                options.method,
                abs_url,
                headers=headers,
                data=data,  # type: ignore
                files=options.files,
                timeout=request_timeout or self.timeout,
            )

            result = await self.async_client.send(
                req, stream=stream, follow_redirects=options.allow_redirects
            )

        except httpx.TimeoutException as e:
            utils.log_debug("Encountered httpx.TimeoutException")

            try:
                resp_headers = dict(result.headers)
            except AttributeError:
                resp_headers = {}

            if remaining_retries > 0:
                return await self._retry_async_request(
                    options,
                    remaining_retries=remaining_retries,
                    response_headers=resp_headers,
                    stream=stream,
                    request_timeout=request_timeout,
                )

            raise error.Timeout("Request timed out: {}".format(e)) from e
        except httpx.RequestError as e:
            utils.log_debug("Encountered httpx.RequestError")

            try:
                resp_headers = dict(result.headers)
            except AttributeError:
                resp_headers = {}

            if remaining_retries > 0:
                return await self._retry_async_request(
                    options,
                    remaining_retries=remaining_retries,
                    response_headers=resp_headers,
                    stream=stream,
                    request_timeout=request_timeout,
                )

            raise error.APIConnectionError(
                "Error communicating with API: {}".format(e)
            ) from e

        # retry on 5XX error or rate-limit
        if 500 <= result.status_code < 600 or result.status_code == 429:
            utils.log_debug(
                f"Encountered status error. Error code: {result.status_code}"
            )

            if remaining_retries > 0:
                return await self._retry_async_request(
                    options,
                    remaining_retries=remaining_retries,
                    response_headers=dict(result.headers),
                    stream=stream,
                    request_timeout=request_timeout,
                )

        utils.log_debug(
            "Together API response",
            path=abs_url,
            response_code=result.status_code,
            processing_ms=result.headers.get("x-total-time"),
            request_id=result.headers.get("CF-RAY"),
        )

        return result

    def _interpret_response(
        self, result: httpx.Response, stream: bool
    ) -> Tuple[TogetherResponse | Iterator[TogetherResponse], bool]:
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
        self, result: httpx.Response, stream: bool
    ) -> (
        tuple[AsyncGenerator[TogetherResponse, None], bool]
        | tuple[TogetherResponse, bool]
    ):
        """Returns the response(s) and a bool indicating whether it is a stream."""
        if stream and "text/event-stream" in result.headers.get("Content-Type", ""):
            return (
                self._interpret_response_line(
                    line, result.status_code, result.headers, stream=True
                )
                async for line in parse_stream_async(result.aiter_lines())
            ), True
        else:
            try:
                await result.aread()
            except (httpx.TimeoutException, asyncio.TimeoutError) as e:
                raise error.Timeout("Request timed out") from e
            except httpx.RequestError as e:
                utils.log_warn(e, body=result.content)
            return (
                self._interpret_response_line(
                    (await result.aread()).decode("utf-8"),
                    result.status_code,
                    result.headers,
                    stream=False,
                ),
                False,
            )

    def _interpret_response_line(
        self, rbody: str, rcode: int, rheaders: Any, stream: bool
    ) -> TogetherResponse:
        # HTTP 204 response code does not have any content in the body.
        if rcode == 204:
            return TogetherResponse({}, rheaders)

        if rcode == 503:
            raise error.ServiceUnavailableError(
                "The server is overloaded or not ready yet.",
                http_status=rcode,
                headers=rheaders,
            )

        try:
            if "text/plain" in rheaders.get("Content-Type", ""):
                data: Dict[str, Any] = {"message": rbody}
            else:
                data = json.loads(rbody)
        except (JSONDecodeError, UnicodeDecodeError) as e:
            raise error.APIError(
                f"Error code: {rcode} -{rbody}",
                http_status=rcode,
                headers=rheaders,
            ) from e
        resp = TogetherResponse(data, rheaders)

        # Handle streaming errors
        if not 200 <= rcode < 300:
            raise self.handle_error_response(resp, rcode, stream_error=stream)
        return resp
