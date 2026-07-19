"""Tests for the logprobs request parameter and top_logprobs response data.

The Together API accepts ``logprobs`` as an integer between 0 and 20: the
number of top tokens to return log probabilities for at each generation
step, instead of only the sampled token (see issue #251). When top-k
logprobs are requested, each choice's ``logprobs`` part carries a
``top_logprobs`` list with one ``{token: logprob}`` dict per generated
token.
"""

import json
import warnings

import pytest
from pydantic import ValidationError

from together.types import ChatCompletionRequest, CompletionRequest
from together.types.chat_completions import ChatCompletionResponse


MESSAGES = [{"role": "user", "content": "Say hello."}]
MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

# Response shape documented for the chat completions API with ``logprobs=3``:
# ``top_logprobs`` is a list with one dict of the top-k alternatives per
# generated token.
TOP_LOGPROBS = [
    {"Hello": -2.6e-06, "hello": -13.5, " Hello": -13.875},
    {".": -4.8e-05, "!": -10.0625, ".\n": -11.4375},
]
RESPONSE_PAYLOAD = {
    "id": "889ee12e7b0b3c67",
    "object": "chat.completion",
    "created": 1709240335,
    "model": MODEL,
    "choices": [
        {
            "index": 0,
            "finish_reason": "eos",
            "logprobs": {
                "tokens": ["Hello", "."],
                "token_logprobs": [-2.6e-06, -4.8e-05],
                "top_logprobs": TOP_LOGPROBS,
            },
            "message": {"role": "assistant", "content": "Hello."},
        }
    ],
    "usage": {"prompt_tokens": 4, "completion_tokens": 2, "total_tokens": 6},
}

# A value the API rejects, used to trigger the range error.
OUT_OF_RANGE = 50
# Stand in for private prompt text, so a leak is easy to spot.
SECRET_PROMPT = "unique prompt text that must not escape into an exception"

RANGE_ERROR_TYPES = {"greater_than_equal", "less_than_equal"}


def _assert_scoped_range_error(error: ValidationError, sent: int) -> None:
    """The error must name the logprobs field and carry only that value.

    Scoping matters for privacy as well as for clarity. A model level
    validator reports the whole request as the offending input, which places
    the prompt or the message list inside the exception, and from there into
    any log line or crash reporter that serializes ``errors()``.
    """
    details = error.errors()
    assert len(details) == 1
    assert details[0]["loc"] == ("logprobs",)
    assert details[0]["type"] in RANGE_ERROR_TYPES
    assert details[0]["input"] == sent


@pytest.mark.parametrize("logprobs", [-1, 21, 100])
def test_chat_request_rejects_out_of_range_logprobs(logprobs: int) -> None:
    with pytest.raises(ValidationError) as excinfo:
        ChatCompletionRequest(model=MODEL, messages=MESSAGES, logprobs=logprobs)

    _assert_scoped_range_error(excinfo.value, logprobs)


@pytest.mark.parametrize("logprobs", [-1, 21, 100])
def test_completion_request_rejects_out_of_range_logprobs(logprobs: int) -> None:
    with pytest.raises(ValidationError) as excinfo:
        CompletionRequest(model=MODEL, prompt="Say hello.", logprobs=logprobs)

    _assert_scoped_range_error(excinfo.value, logprobs)


@pytest.mark.parametrize("logprobs", [0, 1, 20])
def test_chat_request_accepts_in_range_logprobs(logprobs: int) -> None:
    request = ChatCompletionRequest(model=MODEL, messages=MESSAGES, logprobs=logprobs)

    # 0 is a valid value and must survive serialization of the payload.
    assert request.model_dump(exclude_none=True)["logprobs"] == logprobs


@pytest.mark.parametrize("logprobs", [0, 1, 20])
def test_completion_request_accepts_in_range_logprobs(logprobs: int) -> None:
    request = CompletionRequest(model=MODEL, prompt="Say hello.", logprobs=logprobs)

    assert request.model_dump(exclude_none=True)["logprobs"] == logprobs


def test_request_logprobs_defaults_to_omitted() -> None:
    request = ChatCompletionRequest(model=MODEL, messages=MESSAGES)

    assert "logprobs" not in request.model_dump(exclude_none=True)


def test_chat_range_error_leaves_the_messages_out_of_the_exception() -> None:
    """Rejecting a bad logprobs value must not expose the conversation.

    Before this check existed the request reached the server and came back as
    an API error that did not repeat the prompt. A client side check has to
    keep that property, otherwise moving validation earlier would hand user
    text to every logger that records the traceback.
    """
    with pytest.raises(ValidationError) as excinfo:
        ChatCompletionRequest(
            model=MODEL,
            messages=[{"role": "user", "content": SECRET_PROMPT}],
            logprobs=OUT_OF_RANGE,
        )

    assert SECRET_PROMPT not in str(excinfo.value)
    assert SECRET_PROMPT not in json.dumps(excinfo.value.errors(), default=str)


def test_completion_range_error_leaves_the_prompt_out_of_the_exception() -> None:
    with pytest.raises(ValidationError) as excinfo:
        CompletionRequest(model=MODEL, prompt=SECRET_PROMPT, logprobs=OUT_OF_RANGE)

    assert SECRET_PROMPT not in str(excinfo.value)
    assert SECRET_PROMPT not in json.dumps(excinfo.value.errors(), default=str)


def test_top_logprobs_survive_parsing_and_model_dump() -> None:
    """Top-k alternatives must round-trip through the response models.

    ``LogprobsPart`` declares only ``tokens`` and ``token_logprobs`` today, so
    ``top_logprobs`` survives on the SDK's base model setting
    ``extra="allow"``: the value is carried untyped and dumped back unchanged.
    This test pins the round-trip rather than the declaration, so it holds
    either way, and it fails if the field is ever declared with the wrong
    shape, for example as a ``Dict[str, float]`` rather than a list of
    per-token dicts. Open PR #452 proposes declaring it as
    ``List[Dict[str, float]]``, which this test already accepts. It does not
    constrain what the server sends.
    """
    response = ChatCompletionResponse(**RESPONSE_PAYLOAD)

    assert response.choices is not None
    logprobs_part = response.choices[0].logprobs
    assert logprobs_part is not None
    assert logprobs_part.top_logprobs == TOP_LOGPROBS

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        dumped = response.model_dump()

    assert dumped["choices"][0]["logprobs"]["top_logprobs"] == TOP_LOGPROBS
