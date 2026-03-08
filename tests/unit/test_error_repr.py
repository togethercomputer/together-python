"""Tests for TogetherException.__repr__ with non-JSON-serializable headers."""

from __future__ import annotations

import json
from collections import OrderedDict
from typing import Any, Iterator
from unittest.mock import MagicMock

import pytest

from together.error import (
    TogetherException,
    AuthenticationError,
    ResponseError,
    APIError,
)


class FakeMultiDictProxy:
    """Simulates aiohttp's CIMultiDictProxy — not JSON serializable."""

    def __init__(self, data: dict[str, str]) -> None:
        self._data = data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: str) -> str:
        return self._data[key]

    def __repr__(self) -> str:
        return f"<FakeMultiDictProxy({self._data!r})>"


class TestExceptionReprNonSerializable:
    """Verify __repr__ doesn't crash on non-JSON-serializable headers (issue #108)."""

    def test_repr_with_dict_headers(self) -> None:
        """Normal dict headers should still work fine."""
        exc = TogetherException(
            message="test error",
            headers={"Content-Type": "application/json"},
            http_status=400,
            request_id="req-123",
        )
        result = repr(exc)
        assert "TogetherException" in result
        assert "test error" in result

    def test_repr_with_multidict_proxy_headers(self) -> None:
        """CIMultiDictProxy-like headers must not crash repr (issue #108)."""
        fake_headers = FakeMultiDictProxy(
            {"Content-Type": "application/json", "X-Request-Id": "abc"}
        )
        exc = TogetherException(
            message="server error",
            headers=fake_headers,  # type: ignore[arg-type]
            http_status=500,
            request_id="req-456",
        )
        # Before fix: TypeError: Object of type FakeMultiDictProxy
        #             is not JSON serializable
        result = repr(exc)
        assert "TogetherException" in result
        assert "server error" in result

    def test_repr_with_none_headers(self) -> None:
        """None headers (default) should work."""
        exc = TogetherException(message="no headers")
        result = repr(exc)
        assert "TogetherException" in result

    def test_repr_with_string_headers(self) -> None:
        """String headers should work."""
        exc = TogetherException(
            message="string headers", headers="raw-header-string"
        )
        result = repr(exc)
        assert "TogetherException" in result

    def test_repr_with_nested_non_serializable(self) -> None:
        """Dict headers containing non-serializable values should not crash."""
        exc = TogetherException(
            message="nested issue",
            headers={"key": MagicMock()},  # type: ignore[dict-item]
            http_status=502,
        )
        result = repr(exc)
        assert "TogetherException" in result

    def test_repr_output_is_valid_after_fix(self) -> None:
        """repr should produce parseable output (class name + JSON string)."""
        exc = TogetherException(
            message="validation error",
            headers={"Authorization": "Bearer ***"},
            http_status=422,
            request_id="req-789",
        )
        result = repr(exc)
        assert result.startswith("TogetherException(")
        # The inner string should be valid JSON
        inner = result[len("TogetherException(") + 1 : -2]  # strip quotes
        parsed = json.loads(inner)
        assert parsed["status"] == 422
        assert parsed["request_id"] == "req-789"

    def test_subclass_repr_with_non_serializable_headers(self) -> None:
        """Subclasses should also benefit from the fix."""
        fake_headers = FakeMultiDictProxy({"X-Rate-Limit": "100"})

        for ExcClass in (AuthenticationError, ResponseError, APIError):
            exc = ExcClass(
                message="subclass test",
                headers=fake_headers,  # type: ignore[arg-type]
                http_status=429,
            )
            result = repr(exc)
            assert ExcClass.__name__ in result
