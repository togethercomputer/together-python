"""Tests for TogetherException.__repr__ with non-JSON-serializable objects.

Regression tests for https://github.com/togethercomputer/together-python/issues/108
where repr() on a TogetherException crashed with TypeError when headers
contained non-serializable objects like aiohttp's CIMultiDictProxy.
"""

from __future__ import annotations

import json
from typing import Any, Iterator

import pytest

from together.error import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    JSONError,
    RateLimitError,
    ResponseError,
    Timeout,
    TogetherException,
)


class FakeCIMultiDictProxy:
    """Mimics aiohttp's CIMultiDictProxy, which is not JSON-serializable."""

    def __init__(self, data: dict[str, str]) -> None:
        self._data = data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> str:
        return self._data[key]

    def __repr__(self) -> str:
        return f"<CIMultiDictProxy({self._data!r})>"


class TestExceptionReprNonSerializable:
    """repr() must never crash, even with non-JSON-serializable attributes."""

    def test_repr_with_non_serializable_headers(self) -> None:
        """Core bug from issue #108: CIMultiDictProxy headers crash repr()."""
        headers = FakeCIMultiDictProxy({"Content-Type": "application/json"})
        exc = TogetherException(
            message="server error",
            headers=headers,  # type: ignore[arg-type]
            http_status=500,
        )
        # Before fix: TypeError: Object of type FakeCIMultiDictProxy is not
        #             JSON serializable
        result = repr(exc)
        assert "TogetherException" in result
        assert "server error" in result

    def test_repr_with_dict_headers(self) -> None:
        """Normal dict headers must still work (regression check)."""
        exc = TogetherException(
            message="bad request",
            headers={"X-Request-Id": "abc-123"},
            http_status=400,
            request_id="req-1",
        )
        result = repr(exc)
        parsed = json.loads(result.split("(", 1)[1].rsplit(")", 1)[0].strip("'\""))
        assert parsed["status"] == 400
        assert parsed["request_id"] == "req-1"

    def test_repr_with_none_headers(self) -> None:
        """Default None headers (stored as {}) must work."""
        exc = TogetherException(message="oops")
        result = repr(exc)
        assert "TogetherException" in result

    def test_repr_with_string_headers(self) -> None:
        """String headers must work."""
        exc = TogetherException(message="err", headers="raw-header")
        result = repr(exc)
        assert "raw-header" in result

    @pytest.mark.parametrize(
        "exc_class",
        [
            AuthenticationError,
            ResponseError,
            JSONError,
            RateLimitError,
            Timeout,
            APIConnectionError,
            APIError,
        ],
    )
    def test_subclasses_inherit_fix(self, exc_class: type) -> None:
        """All subclasses inherit the safe repr via TogetherException."""
        headers = FakeCIMultiDictProxy({"X-Rate-Limit": "100"})
        exc = exc_class(
            message="subclass test",
            headers=headers,  # type: ignore[arg-type]
            http_status=429,
        )
        result = repr(exc)
        assert exc_class.__name__ in result
