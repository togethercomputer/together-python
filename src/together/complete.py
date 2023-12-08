import json
from typing import Any, Dict, Iterator, List, Optional, Union

import together
from together.types import TogetherResponse
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
        api_key: Optional[str] = None,
        cast: bool = False,
        safety_model: Optional[str] = None,
    ) -> Union[Dict[str, Any], TogetherResponse]:
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
            "safety_model": safety_model,
        }

        # send request
        response = create_post_request(
            url=together.api_base_complete, json=parameter_payload, api_key=api_key
        )

        try:
            response_json = dict(response.json())

        except Exception as e:
            raise together.JSONError(e, http_status=response.status_code)

        if cast:
            return TogetherResponse(**response_json)

        return response_json

    @classmethod
    def create_streaming(
        self,
        prompt: str,
        model: Optional[str] = "",
        max_tokens: Optional[int] = 128,
        stop: Optional[List[str]] = None,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.7,
        top_k: Optional[int] = 50,
        repetition_penalty: Optional[float] = None,
        raw: Optional[bool] = False,
        api_key: Optional[str] = None,
        cast: Optional[bool] = False,
        safety_model: Optional[str] = None,
    ) -> Union[Iterator[str], Iterator[TogetherResponse]]:
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
            "safety_model": safety_model,
        }

        # send request
        response = create_post_request(
            url=together.api_base_complete,
            json=parameter_payload,
            api_key=api_key,
            stream=True,
        )

        output = ""
        client = sse_client(response)
        for event in client.events():
            if cast:
                if event.data != "[DONE]":
                    yield TogetherResponse(**json.loads(event.data))
            elif raw:
                yield str(event.data)
            elif event.data != "[DONE]":
                json_response = dict(json.loads(event.data))
                if "error" in json_response.keys():
                    raise together.ResponseError(
                        json_response["error"],
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


class Completion:
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
        api_key: Optional[str] = None,
        stream: bool = False,
    ) -> Union[
        TogetherResponse, Iterator[TogetherResponse], Iterator[str], Dict[str, Any]
    ]:
        if stream:
            return Complete.create_streaming(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                stop=stop,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
                api_key=api_key,
                cast=True,
            )
        else:
            return Complete.create(
                prompt=prompt,
                model=model,
                max_tokens=max_tokens,
                stop=stop,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                repetition_penalty=repetition_penalty,
                logprobs=logprobs,
                api_key=api_key,
                cast=True,
            )
