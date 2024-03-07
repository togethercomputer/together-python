from typing import Any, Iterator, List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    CompletionChunk,
    CompletionRequest,
    CompletionResponse,
    TogetherClient,
)


class Completions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

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
    ) -> CompletionResponse | Iterator[CompletionChunk]:
        requestor = api_requestor.APIRequestor(
            config=self._client,
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

        response, _, _ = requestor.request(
            method="POST",
            url="/completions",
            params=parameter_payload,
            stream=stream,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (CompletionChunk(**line.data) for line in response)
        assert isinstance(response, TogetherResponse)
        return CompletionResponse(**response.data)


class AsyncCompletions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

    async def create(
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
    ) -> Any:
        requestor = api_requestor.APIRequestor(
            config=self._client,
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

        response, _, _ = requestor.request(
            method="POST",
            url="/completions",
            params=parameter_payload,
            stream=stream,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (CompletionChunk(**line.data) for line in response)
        assert isinstance(response, TogetherResponse)
        return CompletionResponse(**response.data)
