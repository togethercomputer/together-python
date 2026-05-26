import inspect

from together.resources.chat.completions import AsyncChatCompletions, ChatCompletions
from together.types.chat_completions import (
    ChatCompletionRequest,
    ChatCompletionResponse,
)
from together.types.common import LogprobsPart


def test_chat_completion_create_exposes_context_length_behavior() -> None:
    sync_signature = inspect.signature(ChatCompletions.create)
    async_signature = inspect.signature(AsyncChatCompletions.create)

    assert "context_length_exceeded_behavior" in sync_signature.parameters
    assert "context_length_exceeded_behavior" in async_signature.parameters


def test_chat_completion_request_serializes_context_length_behavior() -> None:
    request = ChatCompletionRequest(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": "Hello"}],
        context_length_exceeded_behavior="truncate",
    )

    assert (
        request.model_dump(exclude_none=True)["context_length_exceeded_behavior"]
        == "truncate"
    )


def test_logprobs_part_models_top_logprobs_as_list_per_token() -> None:
    assert "top_logprobs" in LogprobsPart.model_fields

    response = ChatCompletionResponse(
        choices=[
            {
                "logprobs": {
                    "tokens": ["Hello", "."],
                    "token_logprobs": [-0.1, -0.2],
                    "top_logprobs": [
                        {"Hello": -0.1, "Hi": -1.4},
                        {".": -0.2, "!": -1.7},
                    ],
                }
            }
        ]
    )

    assert response.choices is not None
    assert response.choices[0].logprobs is not None
    assert response.choices[0].logprobs.top_logprobs == [
        {"Hello": -0.1, "Hi": -1.4},
        {".": -0.2, "!": -1.7},
    ]
    assert response.model_dump()["choices"][0]["logprobs"]["top_logprobs"] == [
        {"Hello": -0.1, "Hi": -1.4},
        {".": -0.2, "!": -1.7},
    ]
