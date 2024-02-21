from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict

from pydantic import BaseModel

from together.types.common import (
    LogprobsPart,
    FinishReason,
    PromptPart,
    ObjectType,
    UsageData,
    DeltaContent,
)


class ChatCompletionMessage(TypedDict):
    role: str
    content: str


class ResponseFormat(TypedDict):
    type: str
    schema: Dict[str, Any]


class FunctionTool(TypedDict):
    description: str | None = None
    name: str
    parameters: Dict[str, Any] | None = None


class FunctionToolChoice(TypedDict):
    name: str


class Tools(TypedDict):
    type: str
    function: FunctionTool


class ToolChoice(TypedDict):
    type: str
    function: FunctionToolChoice


class ChatCompletionRequest(BaseModel):
    messages: List[ChatCompletionMessage]
    model: str
    max_tokens: str | None = 512
    stop: List[str] | None = None
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    repetition_penalty: float | None = None
    stream: bool = False
    logprobs: int | None = None
    echo: bool | None = None
    n: int | None = None
    safety_model: str | None = None
    response_format: ResponseFormat | None = None
    tools: Tools | None = None
    tool_choice: ToolChoice | None = None


class ChatCompletionChoicesData(BaseModel):
    index: int | None = None
    logprobs: LogprobsPart | None = None
    finish_reason: FinishReason | None = None
    message: ChatCompletionMessage = None | None


class ChatCompletionResponse(BaseModel):
    id: str | None = None
    created: int | None = None
    model: str | None = None
    object: ObjectType | None = None
    choices: List[ChatCompletionChoicesData] | None = None
    prompt: List[PromptPart] | List[None] | None = None
    usage: UsageData | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ChatCompletionChunk(BaseModel):
    id: str | None = None
    object: ObjectType
    created: int
    delta: DeltaContent
    model: str
    usage: UsageData
    finish_reason: FinishReason
