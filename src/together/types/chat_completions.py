from __future__ import annotations

import warnings
from enum import Enum
from typing import Any, Dict, List

from pydantic import model_validator
from typing_extensions import Self

from together.types.abstract import BaseModel
from together.types.common import (
    DeltaContent,
    FinishReason,
    LogprobsPart,
    ObjectType,
    PromptPart,
    UsageData,
)


class MessageRole(str, Enum):
    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"
    TOOL = "tool"


class ResponseFormatType(str, Enum):
    JSON_OBJECT = "json_object"
    JSON_SCHEMA = "json_schema"
    REGEX = "regex"


class FunctionCall(BaseModel):
    name: str | None = None
    arguments: str | None = None


class ToolCalls(BaseModel):
    id: str | None = None
    type: str | None = None
    function: FunctionCall | None = None


class ChatCompletionMessageContentType(str, Enum):
    TEXT = "text"
    IMAGE_URL = "image_url"
    VIDEO_URL = "video_url"
    AUDIO_URL = "audio_url"


class ChatCompletionMessageContentImageURL(BaseModel):
    url: str


class ChatCompletionMessageContentVideoURL(BaseModel):
    url: str


class ChatCompletionMessageContentAudioURL(BaseModel):
    url: str


class ChatCompletionMessageContent(BaseModel):
    type: ChatCompletionMessageContentType
    text: str | None = None
    image_url: ChatCompletionMessageContentImageURL | None = None
    video_url: ChatCompletionMessageContentVideoURL | None = None
    audio_url: ChatCompletionMessageContentAudioURL | None = None


class ChatCompletionMessage(BaseModel):
    role: MessageRole
    content: str | List[ChatCompletionMessageContent] | None = None
    tool_calls: List[ToolCalls] | None = None


class ResponseFormat(BaseModel):
    type: ResponseFormatType
    schema_: Dict[str, Any] | None = None
    pattern: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"type": self.type.value}
        if self.schema_ is not None:
            result["schema"] = self.schema_
        if self.pattern is not None:
            result["pattern"] = self.pattern
        return result


class FunctionTool(BaseModel):
    description: str | None = None
    name: str
    parameters: Dict[str, Any] | None = None


class FunctionToolChoice(BaseModel):
    name: str


class Tools(BaseModel):
    type: str
    function: FunctionTool


class ToolChoice(BaseModel):
    type: str
    function: FunctionToolChoice


class ToolChoiceEnum(str, Enum):
    Auto = "auto"
    Required = "required"


class ChatCompletionRequest(BaseModel):
    # list of messages
    messages: List[ChatCompletionMessage]
    # model name
    model: str
    # stopping criteria: max tokens to generate
    max_tokens: int | None = None
    # stopping criteria: list of strings to stop generation
    stop: List[str] | None = None
    # sampling hyperparameters
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    repetition_penalty: float | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None
    min_p: float | None = None
    logit_bias: Dict[str, float] | None = None
    seed: int | None = None
    # stream SSE token chunks
    stream: bool = False
    # return logprobs
    logprobs: int | None = None
    # echo prompt.
    # can be used with logprobs to return prompt logprobs
    echo: bool | None = None
    # number of output generations
    n: int | None = None
    # moderation model
    safety_model: str | None = None
    # constraints
    response_format: ResponseFormat | None = None
    tools: List[Tools] | None = None
    tool_choice: ToolChoice | ToolChoiceEnum | None = None

    # Raise warning if repetition_penalty is used with presence_penalty or frequency_penalty
    @model_validator(mode="after")
    def verify_parameters(self) -> Self:
        if self.repetition_penalty:
            if self.presence_penalty or self.frequency_penalty:
                warnings.warn(
                    "repetition_penalty is not advisable to be used alongside presence_penalty or frequency_penalty"
                )
        return self


class ChatCompletionChoicesData(BaseModel):
    index: int | None = None
    logprobs: LogprobsPart | None = None
    seed: int | None = None
    finish_reason: FinishReason | None = None
    message: ChatCompletionMessage | None = None


class ChatCompletionResponse(BaseModel):
    # request id
    id: str | None = None
    # object type
    object: ObjectType | None = None
    # created timestamp
    created: int | None = None
    # model name
    model: str | None = None
    # choices list
    choices: List[ChatCompletionChoicesData] | None = None
    # prompt list
    prompt: List[PromptPart] | List[None] | None = None
    # token usage data
    usage: UsageData | None = None


class ChatCompletionDeltaToolCalls(ToolCalls):
    """One tool call fragment inside a streaming delta.

    Streaming splits a single tool call across several chunks, so every
    fragment carries an ``index`` naming the call it belongs to. The
    non-streaming :class:`ToolCalls` has no such field, so the index is
    declared on a streaming-only subclass. Putting it on the shared class
    instead would add an ``index`` key to non-streaming
    :class:`ChatCompletionMessage` dumps, which is why the subclass exists.
    """

    index: int | None = None


class ChatCompletionDeltaContent(DeltaContent):
    """Streaming delta for chat completion chunks.

    The API returns an explicit ``null`` for ``choices[n].delta.tool_calls`` on
    text-only chunks, and for ``function.name`` / ``function.arguments`` inside
    tool-call fragments, where the OpenAI streaming format either omits the
    field or sends an empty string, never ``null``
    (https://github.com/togethercomputer/together-python/issues/160).

    Declaring these as typed optional fields makes ``null`` and *missing* parse
    identically (to ``None``) and validates the items into
    :class:`ChatCompletionDeltaToolCalls`, matching the non-streaming
    :class:`ChatCompletionMessage`, so ``model_dump(exclude_none=True)``
    produces OpenAI-shaped deltas with the nulls omitted.

    ``role`` is declared for the same reason. It is sent on the first chunk of
    a response and left out of later ones, so while it was undeclared a present
    role and an absent one behaved differently for callers. It is typed as
    ``str`` rather than :class:`MessageRole` on purpose: chunks are parsed one
    at a time inside the streaming generator, so an unrecognised role value
    would otherwise raise part way through and end the stream.
    """

    role: str | None = None
    tool_calls: List[ChatCompletionDeltaToolCalls] | None = None


class ChatCompletionChoicesChunk(BaseModel):
    index: int | None = None
    logprobs: float | None = None
    seed: int | None = None
    finish_reason: FinishReason | None = None
    delta: ChatCompletionDeltaContent | None = None


class ChatCompletionChunk(BaseModel):
    # request id
    id: str | None = None
    # object type
    object: ObjectType | None = None
    # created timestamp
    created: int | None = None
    # model name
    model: str | None = None
    # delta content
    choices: List[ChatCompletionChoicesChunk] | None = None
    # finish reason
    finish_reason: FinishReason | None = None
    # token usage data
    usage: UsageData | None = None
