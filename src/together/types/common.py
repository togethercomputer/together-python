from enum import Enum
from typing import List

from pydantic import BaseModel


# Generation finish reason
class FinishReason(str, Enum):
    Length = "length"
    StopSequence = "stop"
    EOS = "eos"
    ToolCalls = "tool_calls"


class UsageData(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ObjectType(str, Enum):
    Completion = "text.completion"
    CompletionChunk = "completion.chunk"
    ChatCompletion = "chat.completion"
    ChatCompletionChunk = "chat.completion.chunk"


class LogprobsPart(BaseModel):
    tokens: List[str | None] | None = None
    token_logprobs: List[float | None] | None = None


class PromptPart(BaseModel):
    text: str | None = None
    logprobs: LogprobsPart | None = None


class DeltaContent(BaseModel):
    content: str | None = None
