from typing import Any, Dict, Optional, Union

from requests import RequestException, Response


class TogetherError(Exception):
    def __init__(
        self,
        message: Optional[
            Union[Exception, str, RequestException]
        ] = "Unknown exception raised",
        http_body: Optional[str] = None,
        http_status: Optional[int] = None,
        json_body: Optional[Any] = None,
        headers: Optional[Union[str, Dict[Any, Any]]] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super(TogetherError, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = (
                    "<Could not decode body as utf-8. "
                    "Please contact us via email at support@together.ai>"
                )

        self._message = message
        self._http_body = http_body
        self._http_status = http_status
        self._json_body = json_body
        self._headers = headers or {}
        self._request_id = request_id

    def __str__(self) -> str:
        msg = self._message
        if self._request_id:
            msg = f"Request {self._request_id}: {self._message}"
        if self._http_status:
            msg += f", HTTP status: {self._http_status}"
        return msg

    def __repr__(self) -> str:
        return "%s(message=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self._http_status,
            self._request_id,
        )


class AuthenticationError(TogetherError):
    pass


class ResponseError(TogetherError):
    pass


class JSONError(TogetherError):
    pass


class InstanceError(TogetherError):
    def __init__(
        self,
        message: Optional[str] = None,
        http_body: Optional[str] = None,
        http_status: Optional[int] = None,
        json_body: Optional[Any] = None,
        headers: Optional[str] = None,
        model: Optional[str] = "model",
    ) -> None:
        message = f"""No running instances for {model}. You can start an instance with one of the following methods:
                  1. navigating to the Together Playground at api.together.ai
                  2. starting one in python using together.Models.start(model_name)
                  3. `$ together models start <MODEL_NAME>` at the command line.
                See `together.Models.list()` in python or `$ together models list` in command line to get an updated list of valid model names.
                """
        super(InstanceError, self).__init__(
            message, http_body, http_status, json_body, headers
        )


class FileTypeError(TogetherError):
    pass


class AttributeError(TogetherError):
    pass


class TogetherErrorHandler:
    def __init__(self, map_dict: dict[int, Any] = None) -> None:
        default_dict = {
            400: {"class": None, "message": None},
            429: {"class": InstanceError, "message": None},
            500: {"class": Exception, "message": "Invalid API key supplied."},
        }

        self.map_dict = map_dict or default_dict
        self.response = None

    def exception(self):
        pass

    def pass_exception(self):
        return self.response, True

    def handle(self, response: Response):
        self.response = response
        if response.status_code in self.map_dict.keys():
            handler_map = self.map_dict[response.status_code]
            handler = handler_map["class"]
            handler_message = handler_map["message"]

            if not handler:
                return self.pass_exception()

            if handler_message:
                raise handler(handler_message)
            else:
                raise handler()

        else:
            return self.response, False
