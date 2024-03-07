from typing import Any, Iterator, List, Dict

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
        response_format: Dict[str, Any] | None = None,
        tools: Dict[str, str | Dict[str, Any]] | None = None,
        tool_choice: str | Dict[str, str | Dict[str, str]] | None = None,
    ) -> ChatCompletionResponse | Iterator[ChatCompletionChunk]:
        requestor = api_requestor.APIRequestor(
            config=self._client,
        )

        parameter_payload = ChatCompletionRequest(
            model=model,
            messages=messages,
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
            response_format=response_format,
            tools=tools,
            tool_choice=tool_choice,
        ).model_dump()

        response, _, _ = requestor.request(
            method="POST",
            url="/chat/completions",
            params=parameter_payload,
            stream=stream,
            headers=self._client.default_headers,
            request_timeout=self._client.timeout,
        )

        if stream:
            # must be an iterator
            assert not isinstance(response, TogetherResponse)
            return (ChatCompletionChunk(**line.data) for line in response)
        assert isinstance(response, TogetherResponse)
        print(response.data)
        return ChatCompletionResponse(**response.data)


class AsyncCompletions:
    def __init__(self, client: TogetherClient) -> None:
        self._client = client

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
        tools: Dict[str, str | Dict[str, Any]] | None = None,
        tool_choice: str | Dict[str, str | Dict[str, str]] | None = None,
    ) -> Any:
        requestor = api_requestor.APIRequestor(
            config=self._client,
        )

        parameter_payload = ChatCompletionRequest(
            model=model,
            messages=messages,
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
            response_format=response_format,
            tools=tools,
            tool_choice=tool_choice,
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
            return (ChatCompletionChunk(**line.data) for line in response)
        assert isinstance(response, TogetherResponse)
        return ChatCompletionResponse(**response.data)
