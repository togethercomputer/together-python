from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from together import error
from together.abstract.api_requestor import APIRequestor
from together.types import TogetherClient


@pytest.mark.asyncio
async def test_async_read_connection_error_raises_api_connection_error():
    requestor = APIRequestor(client=TogetherClient(api_key="fake_api_key"))

    response = MagicMock()
    response.headers = {"Content-Type": "application/json"}
    response.status = 200
    response.read = AsyncMock(side_effect=aiohttp.ClientConnectionError("reset"))

    with pytest.raises(error.APIConnectionError):
        await requestor._interpret_async_response(response, stream=False)
