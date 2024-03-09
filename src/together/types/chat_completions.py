from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from pydantic import Field

from together.types.abstract import BaseModel
from together.types.common import (
    DeltaContent,
    FinishReason,
    LogprobsPart,
    ObjectType,
    PromptPart,
    UsageData,
)


class FunctionCall(BaseModel):
    name: str | None = None
    arguments: str | None = None


class ToolCalls(BaseModel):
    id: str | None = None
    type: str | None = None
    function: FunctionCall | None = None


class ChatCompletionMessage(BaseModel):
    role: str
    content: str | None = None
    tool_calls: List[ToolCalls] | None = None


class ResponseFormat(BaseModel):
    type: str
    schema_: Dict[str, Any] | None = Field(None, alias="schema")


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


class ChatCompletionRequest(BaseModel):
    messages: List[ChatCompletionMessage]
    model: str
    max_tokens: int | None = 512
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
    tools: List[Tools] | None = None
    tool_choice: ToolChoice | ToolChoiceEnum | None = None


class ChatCompletionChoicesData(BaseModel):
    index: int | None = None
    logprobs: LogprobsPart | None = None
    finish_reason: FinishReason | None = None
    message: ChatCompletionMessage | None = None


class ChatCompletionResponse(BaseModel):
    id: str | None = None
    created: int | None = None
    model: str | None = None
    object: ObjectType | None = None
    choices: List[ChatCompletionChoicesData] | None = None
    prompt: List[PromptPart] | List[None] | None = None
    usage: UsageData | None = None


class ChatCompletionChunk(BaseModel):
    id: str | None = None
    object: ObjectType
    created: int
    delta: DeltaContent
    model: str
    usage: UsageData
    finish_reason: FinishReason
