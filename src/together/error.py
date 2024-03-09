from typing import Any, Dict, Optional, Union

from pydantic import Field
from requests import RequestException

from together.types.abstract import BaseModel


class TogetherErrorResponse(BaseModel):
    # error message
    message: str | None = None
    # error type
    type_: str | None = Field(None, alias="type")
    # param causing error
    param: str | None = None
    # error code
    code: str | None = None


class TogetherException(Exception):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        response: Optional[Union[str]] = None,
        headers: Optional[Union[str, Dict[Any, Any]]] = None,
        request_id: Optional[str] = "",
        http_status: Optional[int] = None,
    ) -> None:
        super(TogetherException, self).__init__(message)

        self._message = message
        self.http_status = http_status
        self.headers = headers or {}
        self.request_id = request_id
        self.response = response

    def __repr__(self) -> str:
        return "%s(message=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.http_status,
            self.request_id,
        )


class AuthenticationError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class ResponseError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class JSONError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class InstanceError(TogetherException):
    def __init__(self, model: Optional[str] = "model", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.message = f"""No running instances for {model}.
                You can start an instance with one of the following methods:
                  1. navigating to the Together Playground at api.together.ai
                  2. starting one in python using together.Models.start(model_name)
                  3. `$ together models start <MODEL_NAME>` at the command line.
                See `together.Models.list()` in python or `$ together models list` in command line
                to get an updated list of valid model names.
                """


class RateLimitError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class FileTypeError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class AttributeError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class Timeout(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class APIConnectionError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class InvalidRequestError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class APIError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class ServiceUnavailableError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class DownloadError(TogetherException):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)
