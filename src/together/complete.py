import json
from typing import Any, Dict, Iterator, List, Optional

import together
from together.utils import create_post_request, get_logger, sse_client


logger = get_logger(str(__name__))


class Complete:
    @classmethod
    def create(
        self,
        prompt: str,
        model: Optional[str] = "",
        max_tokens: Optional[int] = 128,
        stop: Optional[List[str]] = [],
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
        logprobs: Optional[int] = None,
    ) -> Dict[str, Any]:
        if model == "":
            model = together.default_text_model

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "repetition_penalty": repetition_penalty,
            "logprobs": logprobs,
        }

        # send request
        response = create_post_request(
            url=together.api_base_complete, json=parameter_payload
        )
        if not response:
            return {}
        try:
            response_json = dict(response.json())

        except Exception as e:
            raise together.JSONError(e, http_status=response.status_code)
        return response_json

    @classmethod
    def create_streaming(
        self,
        prompt: str,
        model: Optional[str] = "",
        max_tokens: Optional[int] = 128,
        stop: Optional[str] = None,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
        raw: Optional[bool] = False,
    ) -> Iterator[str]:
        """
        Prints streaming responses and returns the completed text.
        """

        if model == "":
            model = together.default_text_model

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "repetition_penalty": repetition_penalty,
            "stream_tokens": True,
        }

        # send request
        response = create_post_request(
            url=together.api_base_complete, json=parameter_payload, stream=True
        )
        if not response:
            return {}
        output = ""
        client = sse_client(response)
        for event in client.events():
            if raw:
                yield str(event.data)
            elif event.data != "[DONE]":
                json_response = dict(json.loads(event.data))
                if "error" in json_response.keys():
                    raise together.ResponseError(
                        json_response["error"]["error"],
                        request_id=json_response["error"]["request_id"],
                    )
                elif "choices" in json_response.keys():
                    text = json_response["choices"][0]["text"]
                    output += text
                    yield text
                else:
                    raise together.ResponseError(
                        f"Unknown error occured. Received unhandled response: {event.data}"
                    )
