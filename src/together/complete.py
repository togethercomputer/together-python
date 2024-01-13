import json
from typing import Any, Dict, Iterator, List, Optional, Union

from aiohttp import ClientSession, ClientTimeout

import together
from together.types import TogetherResponse
from together.utils import create_post_request, get_headers, get_logger, sse_client


logger = get_logger(str(__name__))


class Complete:
    @classmethod
    def create(
        cls,
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
        cls,
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
        cls,
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


class AsyncComplete:
    @classmethod
    async def create(
        cls,
        prompt: str,
        model: Optional[str],
        max_tokens: int = 20,
        repetition_penalty: Optional[float] = None,
        stop: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        raw: Optional[bool] = False,
        logprobs: Optional[int] = None,
        safety_model: Optional[str] = None,
        stream: Optional[bool] = False,
        timeout: Optional[int] = 10,
    ) -> Any:
        if model == "":
            model = together.default_text_model

        headers = get_headers()

        # Provide a default value for timeout if it is None
        timeout = timeout or 10
        client_timeout = ClientTimeout(timeout * 60)

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

        async with ClientSession(headers=headers, timeout=client_timeout) as session:
            async with session.post(
                together.api_base_complete, json=parameter_payload
            ) as resp:

                async def streamer() -> Any:
                    # Parse ServerSentEvents
                    async for byte_payload in resp.content:
                        # Skip line
                        if byte_payload == b"\n":
                            continue

                        payload = byte_payload.decode("utf-8")

                        # Event data
                        if payload.startswith("data:"):
                            # Decode payload
                            json_payload = json.loads(
                                payload.lstrip("data:").rstrip("/n")
                            )

                            if raw:
                                yield json_payload
                            else:
                                # Parse payload
                                response = TogetherResponse(**json_payload)

                                yield response

                if stream:
                    return await streamer()
                else:
                    payload = await resp.json()
                    response = TogetherResponse(**payload)
                    return response
