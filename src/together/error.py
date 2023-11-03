from typing import Dict, Optional, Union


class TogetherError(Exception):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        if status_code:
            message = f"[{status_code}] {message}"
        super().__init__(message)


class AuthenticationError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class ResponseError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class JSONError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class FileTypeError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class InstanceError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class ValidationError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class AttributeError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class BadRequestError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class TimeoutError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class NotFoundError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class RateLimitExceededError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


class APIKeyError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)

class ConnectionError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


# Unknown error
class UnknownError(TogetherError):
    def __init__(
        self, message: Union[str, Exception], status_code: Optional[int] = None
    ):
        super().__init__(message, status_code)


def parse_error(
    status_code: int,
    payload: Optional[Dict[str, str]] = None,
    message: Optional[str] = None,
) -> Exception:
    if payload:
        # Try to parse a Text Generation Inference error
        error_message = payload.get("error", "Unknown error")
        if "error_type" in payload:
            error_type = payload["error_type"]
            if error_type == "Timeout":
                return TimeoutError(error_message, status_code)
            elif error_type == "validation":
                return ValidationError(error_message, status_code)

    if message:
        error_message = message
    else:
        error_message = "Unknown error"

    # Try to parse a APIInference error
    if status_code == 302:
        return ResponseError(error_message, status_code)
    if status_code == 400:
        return BadRequestError(error_message, status_code)
    if status_code == 401:
        error_message = "This job would exceed your free trial credits. Please upgrade to a paid account through Settings -> Billing on api.together.ai to continue."
        return AuthenticationError(error_message, status_code)
    if status_code == 429:
        return InstanceError(error_message, status_code)
    if status_code == 500:
        return APIKeyError(error_message, status_code)
    if status_code == 504:
        return TimeoutError(error_message, status_code)
    if status_code == 404:
        return NotFoundError(error_message, status_code)
    if status_code == 429:
        return RateLimitExceededError(error_message, status_code)

    # Fallback to an unknown error
    return UnknownError(error_message, status_code)
