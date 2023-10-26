from typing import Any, Dict, Optional, Union

from requests import RequestException


class TogetherException(Exception):
    def __init__(
        self,
        message: Optional[Union[Exception, str, RequestException]] = "",
        http_body: Optional[str] = None,
        http_status: Optional[int] = None,
        json_body: Optional[Any] = None,
        headers: Optional[Union[str, Dict[Any, Any]]] = None,
        request_id: Optional[str] = "",
    ) -> None:
        super(TogetherException, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = (
                    "<Could not decode body as utf-8. "
                    "Please contact us via email at support@together.ai>"
                )

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.request_id = request_id

    def __repr__(self) -> str:
        return "%s(message=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.http_status,
            self.request_id,
        )


class AuthenticationError(TogetherException):
    pass


class ResponseError(TogetherException):
    pass


class JSONError(TogetherException):
    pass


class InstanceError(TogetherException):
    def __init__(
        self,
        message: Optional[str] = None,
        http_body: Optional[str] = None,
        http_status: Optional[int] = None,
        json_body: Optional[Any] = None,
        headers: Optional[str] = None,
        model: Optional[str] = "model",
    ) -> None:
        message = f"""No running instances for {model}.
                You can start an instance with one of the following methods:
                  1. navigating to the Together Playground at api.together.ai
                  2. starting one in python using together.Models.start(model_name)
                  3. `$ together models start <MODEL_NAME>` at the command line.
                See `together.Models.list()` in python or `$ together models list` in command line
                to get an updated list of valid model names.
                """
        super(InstanceError, self).__init__(
            message, http_body, http_status, json_body, headers
        )


class RateLimitError(TogetherException):
    pass


class FileTypeError(TogetherException):
    pass


class AttributeError(TogetherException):
    pass
