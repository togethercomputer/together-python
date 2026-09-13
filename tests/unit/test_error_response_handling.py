import pytest

from together.abstract.api_requestor import APIRequestor
from together.error import InvalidRequestError, JSONError, RateLimitError
from together.together_response import TogetherResponse


class TestHandleErrorResponse:
    def test_detail_style_body_raises_json_error(self):
        """
        FastAPI-style error bodies ({"detail": ...}) have no "error" object.
        The SDK must raise JSONError, not a raw AssertionError.
        """
        resp = TogetherResponse({"detail": "Not Found"}, {})

        with pytest.raises(JSONError):
            APIRequestor.handle_error_response(resp, 404)

    def test_non_dict_error_field_raises_json_error(self):
        resp = TogetherResponse({"error": "bad request"}, {})

        with pytest.raises(JSONError):
            APIRequestor.handle_error_response(resp, 400)

    def test_non_dict_body_raises_json_error(self):
        resp = TogetherResponse(["unexpected", "list"], {})

        with pytest.raises(JSONError):
            APIRequestor.handle_error_response(resp, 500)

    def test_valid_error_body_maps_status_codes(self):
        body = {"error": {"message": "rate limited", "type": "rate_limit"}}
        resp = TogetherResponse(body, {})

        assert isinstance(
            APIRequestor.handle_error_response(resp, 429), RateLimitError
        )
        assert isinstance(
            APIRequestor.handle_error_response(resp, 400), InvalidRequestError
        )
