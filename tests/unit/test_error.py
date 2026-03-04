from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

from together.error import TogetherException


class TestTogetherExceptionRepr:
    def test_repr_with_dict_headers(self):
        """Test __repr__ works with standard dict headers."""
        exc = TogetherException(
            message="test error",
            headers={"Content-Type": "application/json"},
            http_status=400,
            request_id="req-123",
        )
        result = repr(exc)
        assert "TogetherException" in result
        assert "test error" in result

    def test_repr_with_non_serializable_headers(self):
        """
        Test __repr__ does not crash when headers contain
        non-JSON-serializable objects (e.g. CIMultiDictProxy).

        Regression test for https://github.com/togethercomputer/together-python/issues/108
        """

        class NonSerializable:
            """A class that is not JSON serializable."""

            def __str__(self) -> str:
                return "NonSerializable()"

        exc = TogetherException(
            message="test error",
            headers=NonSerializable(),
            http_status=500,
            request_id="req-456",
        )
        # Should not raise TypeError
        result = repr(exc)
        assert "TogetherException" in result
        assert "NonSerializable()" in result

    def test_repr_with_mock_cimultidictproxy(self):
        """
        Test __repr__ handles an object mimicking aiohttp's
        CIMultiDictProxy, which triggered the original bug.
        """
        mock_headers = MagicMock()
        mock_headers.__str__ = lambda self: "{'key': 'value'}"

        exc = TogetherException(
            message="connection error",
            headers=mock_headers,
            http_status=502,
        )
        # Should not raise TypeError
        result = repr(exc)
        assert "TogetherException" in result

    def test_repr_with_none_headers(self):
        """Test __repr__ works when headers is None (default)."""
        exc = TogetherException(message="test error")
        result = repr(exc)
        assert "TogetherException" in result

    def test_repr_output_is_valid_json_inside(self):
        """Test that the JSON portion inside __repr__ is valid."""
        exc = TogetherException(
            message="test error",
            headers={"X-Request-Id": "abc"},
            http_status=429,
            request_id="req-789",
        )
        result = repr(exc)
        # Extract the JSON string from repr output: ClassName('json_string')
        # The format is: TogetherException('{"response": ...}')
        json_start = result.index("'") + 1
        json_end = result.rindex("'")
        json_str = result[json_start:json_end]
        parsed = json.loads(json_str)
        assert parsed["status"] == 429
        assert parsed["request_id"] == "req-789"
