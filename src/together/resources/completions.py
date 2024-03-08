from typing import Generator, Iterator, List

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
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

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

        response, _, _ = self.requestor.request(
            method="POST",
            url="/completions",
            params=parameter_payload,
            stream=stream,
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
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

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
    ) -> Generator[CompletionChunk, None, None] | CompletionResponse:
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

        response, _, _ = await self.requestor.arequest(
            method="POST",
            url="/completions",
            params=parameter_payload,
            stream=stream,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (CompletionChunk(**line.data) async for line in response)
        assert isinstance(response, TogetherResponse)
        return CompletionResponse(**response.data)
