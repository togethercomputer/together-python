import logging
from unittest.mock import AsyncMock

import pytest

import together
from together.abstract.api_requestor import APIRequestor
from together.types import TogetherClient, TogetherRequest


def test_debug_request_logs_exclude_secrets(caplog, capsys, monkeypatch):
    monkeypatch.setattr(together, "log", "debug")
    client = TogetherClient(api_key="secret-api-key")
    requestor = APIRequestor(client)
    with caplog.at_level(logging.DEBUG, logger="together"):
        url, headers, data = requestor._prepare_request_raw(
            TogetherRequest(
                method="POST",
                url="https://user:secret-password@example.com/images?token=secret-query",
                headers={"X-Custom-Auth": "secret-header"},
                params={"prompt": "private-prompt", "wandb_api_key": "secret-wandb"},
            ),
            absolute=True,
        )
    logs = caplog.text + capsys.readouterr().err
    for secret in [
        "secret-api-key",
        "secret-password",
        "secret-query",
        "secret-header",
        "private-prompt",
        "secret-wandb",
    ]:
        assert secret not in logs
    assert "path=/images" in logs
    assert headers["Authorization"] == "Bearer secret-api-key"
    assert headers["X-Custom-Auth"] == "secret-header"
    assert "secret-query" in url
    assert b"private-prompt" in data


@pytest.mark.asyncio
async def test_async_response_logs_exclude_headers_and_body(
    caplog, capsys, monkeypatch
):
    monkeypatch.setattr(together, "log", "debug")
    session = AsyncMock()
    response = session.request.return_value
    response.status = 200
    response.headers = {"Set-Cookie": "secret-cookie"}
    response.content = "private-response"
    with caplog.at_level(logging.DEBUG, logger="together"):
        result = await APIRequestor(
            TogetherClient(api_key="secret-api-key")
        ).arequest_raw(
            TogetherRequest(method="GET", url="images?token=secret-query"), session
        )
    logs = caplog.text + capsys.readouterr().err
    for secret in [
        "secret-api-key",
        "secret-query",
        "secret-cookie",
        "private-response",
    ]:
        assert secret not in logs
    assert result is response


def test_client_repr_excludes_credentials():
    client = TogetherClient(
        api_key="secret-api-key", supplied_headers={"Authorization": "secret-header"}
    )
    assert "secret-api-key" not in repr(client)
    assert "secret-header" not in repr(client)
