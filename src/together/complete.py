import json
import warnings
from typing import Iterator, List, Optional, Union, AsyncIterator

import requests
from aiohttp import ClientSession, ClientTimeout
from pydantic import ValidationError

import together
from together.error import ResponseError, parse_error
from together.tools.types import (
    Parameters,
    TogetherResponse,
)
from together.utils import get_headers


class Complete:
    @classmethod
    def create(
        self,
        prompt: str,
        model: Optional[str],
        max_tokens: int = 20,
        repetition_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        stop: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        details: Optional[bool] = False,
        stream: Optional[bool] = False,
        raw: Optional[bool] = False,
    ) -> Union[TogetherResponse, Iterator[TogetherResponse]]:
        if model is None:
            model = together.default_text_model
        parameters = Parameters(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            repetition_penalty=repetition_penalty,
            seed=seed,
            stop=stop if stop is not None else [],
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stream_tokens=stream,
            details=details,
        ).model_dump()

        headers = get_headers()

        resp = requests.post(
            together.api_base_complete, json=parameters, headers=headers, stream=stream
        )

        if resp.status_code != 200:
            try:
                err_payload = resp.json()
            except Exception:
                err_payload = None
            raise parse_error(resp.status_code, err_payload)

        def streamer() -> Iterator[TogetherResponse]:
            # Parse ServerSentEvents
            for byte_payload in resp.iter_lines():
                payload = byte_payload.decode("utf-8")

                # Event data
                if payload.startswith("data:"):
                    if payload == "data: [DONE]":
                        break
                    # Decode payload
                    json_payload = json.loads(payload.lstrip("data:"))

                    if raw:
                        yield json_payload
                    else:
                        # Parse payload
                        try:
                            response = TogetherResponse(**json_payload)
                        except ValidationError:
                            # If we failed to parse the payload, then it is an error payload
                            raise parse_error(resp.status_code, json_payload)

                        # check if key `error` exists and parse the error
                        if response.error:
                            raise parse_error(resp.status_code, json_payload)
                        yield response

        if stream:
            return streamer()
        else:
            payload = dict(resp.json())
            response = TogetherResponse(**payload)
            if response.error:
                raise parse_error(resp.status_code, payload)
            return response

    @classmethod
    def create_streaming(
        self,
        prompt: str,
        model: Optional[str],
        max_tokens: int = 20,
        repetition_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        stop: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        raw: Optional[bool] = False,
    ) -> Iterator[str]:
        warnings.warn(
            "Call to deprecated function create_streaming() and will be removed in v3.0.0 of Together. Use create() with stream=True instead."
        )
        if model is None:
            model = together.default_text_model
        parameters = Parameters(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            repetition_penalty=repetition_penalty,
            seed=seed,
            stop=stop if stop is not None else [],
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stream_tokens=True,
        ).model_dump()

        headers = get_headers()

        resp = requests.post(
            together.api_base_complete, json=parameters, headers=headers, stream=True
        )

        # # Parse ServerSentEvents
        for byte_payload in resp.iter_lines():
            payload = str(byte_payload.decode("utf-8"))
            if raw:
                yield str(payload)
            elif payload != "data: [DONE]":
                if payload.startswith("data: "):
                    payload = payload[len("data: ") :]  # truncate `data: ` from payload
                else:
                    continue

                json_response = dict(json.loads(payload))
                if "error" in json_response.keys():
                    raise ResponseError(
                        json_response["error"]["error"],
                    )
                elif "choices" in json_response.keys():
                    text = json_response["choices"][0]["text"]
                    yield text
                else:
                    raise ResponseError(
                        f"Unknown error occured. Received unhandled response: {payload}"
                    )


class AsyncClient:
    @classmethod
    async def create(
        self,
        prompt: str,
        model: Optional[str],
        max_tokens: int = 20,
        repetition_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        stop: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        top_k: Optional[int] = None,
        top_p: Optional[float] = None,
        raw: Optional[bool] = False,
        stream: Optional[bool] = False,
        timeout: Optional[int] = 10,
    ) -> requests.Response:
        if model is None:
            model = together.default_text_model
        # Validate parameters
        parameters = Parameters(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            repetition_penalty=repetition_penalty,
            seed=seed,
            stop=stop if stop is not None else [],
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stream_tokens=stream,
        ).model_dump()

        headers = get_headers()

        client_timeout = ClientTimeout(timeout * 60)

        async with ClientSession(headers=headers, timeout=client_timeout) as session:
            async with session.post(
                together.api_base_complete, json=parameters
            ) as resp:
                payload = await resp.json()

                if resp.status != 200:
                    raise parse_error(resp.status, payload)
                
                async def streamer():
                    # Parse ServerSentEvents
                    async for byte_payload in resp.content:
                        # Skip line
                        if byte_payload == b"\n":
                            continue

                        payload = byte_payload.decode("utf-8")

                        # Event data
                        if payload.startswith("data:"):
                            # Decode payload
                            json_payload = json.loads(payload.lstrip("data:").rstrip("/n"))

                            if raw:
                                yield json_payload
                            else:
                                # Parse payload
                                try:
                                    response = TogetherResponse(**json_payload)
                                except ValidationError:
                                    # If we failed to parse the payload, then it is an error payload
                                    raise parse_error(resp.status, json_payload)
                                yield response
                if stream:
                    return await streamer()
                else:
                    payload = dict(resp.json())
                    response = TogetherResponse(**payload)
                    if response.error:
                        raise parse_error(resp.status_code, payload)
                    return await response
