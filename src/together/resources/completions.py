from typing import Any, Iterator, List, Optional, Union

import together
from together.together_response import TogetherResponse
from together.abstract import api_requestor
from together.utils import default_api_key

from ..types import CompletionsResponse


class Completions:
    @classmethod
    def create(
            cls,
            prompt: str,
            model: str,
            max_tokens: Optional[int] = 512,
            stop: Optional[List[str]] = [],
            temperature: Optional[float] = 0.7,
            top_p: Optional[float] = 0.7,
            top_k: Optional[int] = 50,
            repetition_penalty: Optional[float] = None,
            safety_model: Optional[str] = None,
            stream: bool = False,
            api_key: Optional[str] = None,
            api_base: Optional[str] = None,
    ) -> Union[CompletionsResponse, Iterator[CompletionsResponse]]:
        requestor = api_requestor.APIRequestor(
            key=api_key,
            api_base=api_base
        )

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "repetition_penalty": repetition_penalty,
            "safety_model": safety_model,
            "stream": stream
        }

        response, got_stream, api_key = requestor.request(
            method="POST",
            url="/completions",
            params=parameter_payload,
            stream=stream
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (
                CompletionsResponse(**line.data) for line in response
            )

        print(response.data)
        return CompletionsResponse(**response.data)

    @classmethod
    def create_streaming(cls, prompt: str, model: str, *args, **kwargs):
        import warnings
        warnings.warn("The 'create_streaming' method is deprecated, "
                      "use 'create' instead", DeprecationWarning, 2)
        kwargs['stream'] = True
        return cls.create(prompt, model, *args, **kwargs)


class AsyncCompletions:
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
        safety_model: Optional[str] = None,
        stream: Optional[bool] = False,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
    ) -> Any:
        requestor = api_requestor.APIRequestor(
            key=api_key,
            api_base=api_base
        )

        parameter_payload = {
            "model": model,
            "prompt": prompt,
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop": stop,
            "repetition_penalty": repetition_penalty,
            "safety_model": safety_model,
        }

        response, got_stream, api_key = requestor.arequest(
            method="POST",
            url=together.api_base_complete,
            params=parameter_payload,
            stream=stream
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (
                line for line in response
            )

        return response
