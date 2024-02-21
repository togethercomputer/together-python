from typing import List

from pydantic import BaseModel

from together.types.common import (
    DeltaContent,
    FinishReason,
    LogprobsPart,
    ObjectType,
    PromptPart,
    UsageData,
)


class CompletionRequest(BaseModel):
    prompt: str
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


class CompletionChoicesData(BaseModel):
    index: int
    logprobs: LogprobsPart | None = None
    finish_reason: FinishReason
    text: str


class CompletionChoicesChunk(BaseModel):
    index: int
    logprobs: float | None = None
    finish_reason: FinishReason | None = None
    delta: DeltaContent | None = None


class CompletionResponse(BaseModel):
    id: str | None = None
    created: int | None = None
    model: str | None = None
    object: ObjectType | None = None
    choices: List[CompletionChoicesData] | None = None
    prompt: List[PromptPart] | None = None
    usage: UsageData | None = None


class CompletionChunk(BaseModel):
    id: str | None = None
    object: ObjectType | None = None
    created: int | None = None
    choices: List[CompletionChoicesChunk] | None = None
    model: str | None = None
    usage: UsageData | None = None
