"""Regression tests for https://github.com/togethercomputer/together-python/issues/160

The Together API returns an explicit ``null`` where the OpenAI streaming format
either leaves the field out or sends an empty string, in three known places:

1. ``choices[n].delta.tool_calls`` (text-only chunks, left out by OpenAI)
2. ``choices[n].delta.tool_calls[n].function.arguments`` (first tool-call chunk,
   where only the name is given; OpenAI sends an empty string here so that
   consumers can concatenate every fragment without a special case)
3. ``choices[n].delta.tool_calls[n].function.name`` (continuation chunks that
   stream the JSON arguments incrementally, left out by OpenAI)

``choices[n].delta.role`` has the same shape of problem from the other
direction: it is sent on the first chunk and left out of the rest, so while it
was undeclared a present role and an absent one behaved differently.

These tests pin down that the parsed models normalize ``null`` to be
indistinguishable from a missing field, so OpenAI-compatible consumers do not
need Together-specific special cases.
"""

from together.types import ChatCompletionChunk, ChatCompletionResponse
from together.types.chat_completions import FunctionCall, ToolCalls


def _chunk(delta: dict) -> ChatCompletionChunk:
    """Build a chunk the way the SDK does: ChatCompletionChunk(**line.data)."""
    return ChatCompletionChunk(
        **{
            "id": "884581f24f0cfdd0-SJC",
            "object": "chat.completion.chunk",
            "created": 1725561260,
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "choices": [{"index": 0, "delta": delta, "finish_reason": None}],
        }
    )


# Wire payloads as observed in issue #160
TEXT_ONLY_DELTA_WITH_NULL = {
    "role": "assistant",
    "content": "Hello",
    "tool_calls": None,
}
TEXT_ONLY_DELTA_OMITTED = {"role": "assistant", "content": "Hello"}
FIRST_TOOL_CALL_DELTA = {
    "role": "assistant",
    "content": None,
    "tool_calls": [
        {
            "index": 0,
            "id": "call_f7g2h8i9j0",
            "type": "function",
            "function": {"name": "get_current_weather", "arguments": None},
        }
    ],
}
CONTINUATION_TOOL_CALL_DELTA = {
    "tool_calls": [
        {
            "index": 0,
            "function": {"name": None, "arguments": '{"location": "San Fra'},
        }
    ]
}


def _has_no_none_values(obj: object) -> bool:
    if obj is None:
        return False
    if isinstance(obj, dict):
        return all(_has_no_none_values(v) for v in obj.values())
    if isinstance(obj, list):
        return all(_has_no_none_values(v) for v in obj)
    return True


def test_null_tool_calls_parses_like_omitted_tool_calls() -> None:
    """`tool_calls: null` (text-only chunks) must behave exactly like a
    missing `tool_calls` field: attribute exists and is None in both cases."""
    with_null = _chunk(TEXT_ONLY_DELTA_WITH_NULL).choices[0].delta
    omitted = _chunk(TEXT_ONLY_DELTA_OMITTED).choices[0].delta

    assert with_null is not None and omitted is not None
    assert with_null.tool_calls is None
    assert omitted.tool_calls is None  # was AttributeError before the fix
    assert with_null.content == omitted.content == "Hello"


def test_tool_call_delta_items_are_typed_models() -> None:
    """Streaming tool-call fragments parse into the same ToolCalls/FunctionCall
    models used by the non-streaming ChatCompletionMessage."""
    delta = _chunk(FIRST_TOOL_CALL_DELTA).choices[0].delta
    assert delta is not None and delta.tool_calls is not None

    (tool_call,) = delta.tool_calls
    assert isinstance(tool_call, ToolCalls)
    assert isinstance(tool_call.function, FunctionCall)
    assert tool_call.id == "call_f7g2h8i9j0"
    assert tool_call.type == "function"
    assert tool_call.function.name == "get_current_weather"
    # null arguments on the first chunk normalizes to None (absent)
    assert tool_call.function.arguments is None


def test_null_function_name_on_continuation_chunks() -> None:
    """`function.name: null` on argument-continuation chunks normalizes to
    None while the incremental arguments fragment is preserved verbatim."""
    delta = _chunk(CONTINUATION_TOOL_CALL_DELTA).choices[0].delta
    assert delta is not None and delta.tool_calls is not None

    (tool_call,) = delta.tool_calls
    assert tool_call.function is not None
    assert tool_call.function.name is None
    assert tool_call.function.arguments == '{"location": "San Fra'


def test_exclude_none_dump_produces_openai_shaped_deltas() -> None:
    """model_dump(exclude_none=True) must omit every API-provided null,
    including the ones nested inside tool_calls[n].function."""
    for wire_delta in (
        TEXT_ONLY_DELTA_WITH_NULL,
        TEXT_ONLY_DELTA_OMITTED,
        FIRST_TOOL_CALL_DELTA,
        CONTINUATION_TOOL_CALL_DELTA,
    ):
        delta = _chunk(wire_delta).choices[0].delta
        assert delta is not None
        dumped = delta.model_dump(exclude_none=True)
        assert _has_no_none_values(dumped), f"None survived in {dumped!r}"

    text_only = _chunk(TEXT_ONLY_DELTA_WITH_NULL).choices[0].delta
    assert text_only is not None
    assert "tool_calls" not in text_only.model_dump(exclude_none=True)


def test_role_parses_the_same_whether_sent_or_left_out() -> None:
    """`delta.role` is sent on the first chunk and left out of later ones, so
    both must give the same attribute rather than one raising AttributeError."""
    first = _chunk(TEXT_ONLY_DELTA_WITH_NULL).choices[0].delta
    later = _chunk(CONTINUATION_TOOL_CALL_DELTA).choices[0].delta

    assert first is not None and later is not None
    assert first.role == "assistant"
    assert later.role is None  # was AttributeError before the fix
    # An unrecognised role must not end the stream, which is why the field is
    # typed as str rather than the MessageRole enum.
    assert _chunk({"role": "some_future_role"}).choices[0].delta.role == (
        "some_future_role"
    )


def test_tool_call_index_is_typed_on_the_streaming_model_only() -> None:
    """Streaming splits one tool call across chunks, so `index` says which call
    a fragment belongs to.

    It is declared on a streaming-only subclass. Declaring it on the shared
    ToolCalls instead would add an `index` key to non-streaming message dumps,
    so this pins the separation in both directions.
    """
    delta = _chunk(FIRST_TOOL_CALL_DELTA).choices[0].delta
    assert delta is not None and delta.tool_calls is not None

    (tool_call,) = delta.tool_calls
    assert isinstance(tool_call, ToolCalls)
    assert tool_call.index == 0
    assert "index" in type(tool_call).model_fields
    assert "index" not in ToolCalls.model_fields
    assert delta.model_dump(exclude_none=True)["tool_calls"][0]["index"] == 0


def test_undeclared_wire_fields_are_still_preserved() -> None:
    """Fields the SDK does not declare must keep flowing through, as they did
    before the fix (extra="allow"), so new API fields are never dropped."""
    delta = (
        _chunk({"role": "assistant", "content": "Hi", "future_field": 7})
        .choices[0]
        .delta
    )
    assert delta is not None
    assert delta.future_field == 7  # type: ignore[attr-defined]
    assert delta.model_dump(exclude_none=True)["future_field"] == 7


def test_non_streaming_tool_calls_unchanged() -> None:
    """Non-streaming responses keep parsing tool_calls into typed models."""
    response = ChatCompletionResponse(
        **{
            "id": "884581f24f0cfdd0-SJC",
            "object": "chat.completion",
            "created": 1725561260,
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "tool_calls",
                    "message": {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_f7g2h8i9j0",
                                "type": "function",
                                "function": {
                                    "name": "get_current_weather",
                                    "arguments": '{"location": "San Francisco, CA"}',
                                },
                            }
                        ],
                    },
                }
            ],
        }
    )
    assert response.choices is not None
    message = response.choices[0].message
    assert message is not None and message.tool_calls is not None
    assert isinstance(message.tool_calls[0], ToolCalls)
    assert message.tool_calls[0].function is not None
    assert message.tool_calls[0].function.name == "get_current_weather"
