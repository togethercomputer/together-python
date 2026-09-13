from unittest.mock import patch

import aiohttp
import pytest

from together.abstract.api_requestor import APIRequestor
from together.error import APIConnectionError, Timeout
from together.types import TogetherClient


class _FailingReadResponse:
    """Minimal stand-in for aiohttp.ClientResponse whose read() fails."""

    status = 200
    headers = {"Content-Type": "application/json"}
    content = None

    def __init__(self, exc):
        self._exc = exc

    async def read(self):
        raise self._exc

    def release(self):
        pass


class TestAsyncResponseReadErrors:
    @pytest.fixture
    def requestor(self):
        with patch.dict("os.environ", {"TOGETHER_API_KEY": "fake_api_key"}):
            return APIRequestor(client=TogetherClient(api_key="fake_api_key"))

    @pytest.mark.asyncio
    async def test_client_error_reading_body_raises_connection_error(self, requestor):
        """
        A connection failure while reading a non-streaming response body must
        surface as APIConnectionError, not UnboundLocalError.
        """
        resp = _FailingReadResponse(aiohttp.ClientError("connection reset"))

        with pytest.raises(APIConnectionError):
            await requestor._interpret_async_response(resp, stream=False)

    @pytest.mark.asyncio
    async def test_timeout_reading_body_raises_timeout(self, requestor):
        resp = _FailingReadResponse(aiohttp.ServerTimeoutError("read timeout"))

        with pytest.raises(Timeout):
            await requestor._interpret_async_response(resp, stream=False)
