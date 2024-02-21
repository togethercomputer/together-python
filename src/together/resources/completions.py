from typing import Any, Iterator, List, Mapping, Optional, Union

import together
from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import CompletionChunk, CompletionRequest, CompletionResponse


class Completions:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        default_headers: Mapping[str, str] | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers

    def create(
        self,
        prompt: str,
        model: str,
        max_tokens: int | None = 512,
        stop: List[str] | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        top_k: int | None = None,
        repetition_penalty: float | None = None,
        stream: bool = False,
        logprobs: int | None = None,
        echo: bool | None = None,
        n: int | None = None,
        safety_model: str | None = None,
        api_key: str | None = None,
        api_base: str | None = None,
    ) -> Union[CompletionResponse, Iterator[CompletionChunk]]:
        print(self.base_url)
        requestor = api_requestor.APIRequestor(
            key=api_key or self.api_key,
            api_base=api_base or self.base_url,
            max_retries=self.max_retries,
        )

        parameter_payload = CompletionRequest(
            model=model,
            prompt=prompt,
            top_p=top_p,
            top_k=top_k,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
            repetition_penalty=repetition_penalty,
            stream=stream,
            logprobs=logprobs,
            echo=echo,
            n=n,
            safety_model=safety_model,
        ).model_dump()

        print(parameter_payload)

        response, _, api_key = requestor.request(
            method="POST",
            url="/completions",
            params=parameter_payload,
            stream=stream,
            headers=self.default_headers,
            request_timeout=self.timeout,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, CompletionResponse)
            return (CompletionChunk(**line.data) for line in response)

        return CompletionResponse(**response.data)

    @classmethod
    def create_streaming(cls, prompt: str, model: str, *args, **kwargs):
        import warnings

        warnings.warn(
            "The 'create_streaming' method is deprecated, " "use 'create' instead",
            DeprecationWarning,
            2,
        )
        kwargs["stream"] = True
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
        requestor = api_requestor.APIRequestor(key=api_key, api_base=api_base)

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
            stream=stream,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (line for line in response)

        return response
