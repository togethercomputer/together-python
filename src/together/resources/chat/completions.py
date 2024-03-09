from typing import Any, AsyncGenerator, Dict, Iterator, List

from together.abstract import api_requestor
from together.together_response import TogetherResponse
from together.types import (
    ChatCompletionChunk,
    ChatCompletionRequest,
    ChatCompletionResponse,
    TogetherClient,
)


class ChatCompletions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    def create(
        self,
        messages: List[Dict[str, str]],
        model: str,
        max_tokens: int | None = None,
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
        response_format: Dict[str, str | Dict[str, Any]] | None = None,
        tools: Dict[str, str | Dict[str, Any]] | None = None,
        tool_choice: str | Dict[str, str | Dict[str, str]] | None = None,
    ) -> ChatCompletionResponse | Iterator[ChatCompletionChunk]:
        parameter_payload = ChatCompletionRequest(
            model=model,
            messages=messages,  # type: ignore
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
            response_format=response_format,  # type: ignore
            tools=tools,  # type: ignore
            tool_choice=tool_choice,  # type: ignore
        ).model_dump()

        response, _, _ = self.requestor.request(
            method="POST",
            url="/chat/completions",
            params=parameter_payload,
            stream=stream,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (ChatCompletionChunk(**line.data) for line in response)
        assert isinstance(response, TogetherResponse)
        print(response.data)
        return ChatCompletionResponse(**response.data)


class AsyncChatCompletions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client
        self.requestor = api_requestor.APIRequestor(
            client=self._client,
        )

    async def create(
        self,
        messages: List[Dict[str, str]],
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
        response_format: Dict[str, Any] | None = None,
        tools: Dict[str, str | Dict[str, str | Dict[str, Any]]] | None = None,
        tool_choice: str | Dict[str, str | Dict[str, str]] | None = None,
    ) -> AsyncGenerator[ChatCompletionChunk, None] | ChatCompletionResponse:
        parameter_payload = ChatCompletionRequest(
            model=model,
            messages=messages,  # type: ignore
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
            response_format=response_format,  # type: ignore
            tools=tools,  # type: ignore
            tool_choice=tool_choice,  # type: ignore
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
            return (ChatCompletionChunk(**line.data) async for line in response)
        assert isinstance(response, TogetherResponse)
        return ChatCompletionResponse(**response.data)
