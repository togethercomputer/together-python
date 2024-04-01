from __future__ import annotations

from typing import List

from together.types.abstract import BaseModel
from together.types.common import (
    DeltaContent,
    FinishReason,
    LogprobsPart,
    ObjectType,
    PromptPart,
    UsageData,
)


class CompletionRequest(BaseModel):
    # prompt to complete
    prompt: str
    # query model
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


class CompletionChoicesData(BaseModel):
    index: int
    logprobs: LogprobsPart | None = None
    finish_reason: FinishReason
    text: str


class CompletionChoicesChunk(BaseModel):
    index: int | None = None
    logprobs: float | None = None
    finish_reason: FinishReason | None = None
    delta: DeltaContent | None = None


class CompletionResponse(BaseModel):
    # request id
    id: str | None = None
    # object type
    object: ObjectType | None = None
    # created timestamp
    created: int | None = None
    # model name
    model: str | None = None
    # choices list
    choices: List[CompletionChoicesData] | None = None
    # prompt list
    prompt: List[PromptPart] | None = None
    # token usage data
    usage: UsageData | None = None


class CompletionChunk(BaseModel):
    # request id
    id: str | None = None
    # object type
    object: ObjectType | None = None
    # created timestamp
    created: int | None = None
    # model name
    model: str | None = None
    # choices list
    choices: List[CompletionChoicesChunk] | None = None
    # token usage data
    usage: UsageData | None = None
