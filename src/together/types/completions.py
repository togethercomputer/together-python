import typing
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# Decoder input tokens
class InputToken(BaseModel):
    # Token ID from the model tokenizer
    id: int
    # Token text
    text: str
    # Logprob
    # Optional since the logprob of the first token cannot be computed
    logprob: Optional[float]


# Generated tokens
class Token(BaseModel):
    # Token ID
    id: int
    # Logprob
    logprob: Optional[float]
    # Is the token a special token
    # Can be used to ignore tokens when concatenating
    special: bool


# Generation finish reason
class FinishReason(str, Enum):
    # number of generated tokens == `max_new_tokens`
    Length = "length"
    # the model generated a text included in `stop_sequences`
    StopSequence = "stop"


# Additional sequences when using the `best_of` parameter
class BestOfSequence(BaseModel):
    # Generated text
    generated_text: str
    # Generation finish reason
    finish_reason: FinishReason
    # Number of generated tokens
    generated_tokens: int
    # Sampling seed if sampling was activated
    seed: Optional[int]
    # Decoder input tokens, empty if decoder_input_details is False
    prefill: List[InputToken]
    # Generated tokens
    tokens: List[Token]


# `generate` details
class Details(BaseModel):
    # Generation finish reason
    finish_reason: FinishReason
    # Number of generated tokens
    generated_tokens: int
    # Sampling seed if sampling was activated
    seed: Optional[int]
    # Decoder input tokens, empty if decoder_input_details is False
    prefill: List[InputToken]
    # Generated tokens
    tokens: List[Token]
    # Additional sequences when using the `best_of` parameter
    best_of_sequences: Optional[List[BestOfSequence]]


# `generate` return value
class Response(BaseModel):
    # Generated text
    generated_text: str
    # Generation details
    details: Details


class Choice(BaseModel):
    # Generated text
    text: str
    finish_reason: Optional[FinishReason] = None
    logprobs: Optional[List[float]] = None


# `generate_stream` details
class StreamDetails(BaseModel):
    # Number of generated tokens
    generated_tokens: int
    # Sampling seed if sampling was activated
    seed: Optional[int]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


# `generate_stream` return value
class CompletionsResponse(BaseModel):
    id: Optional[str] = None
    choices: Optional[List[Choice]] = None
    generated_text: Optional[str] = None
    # Generation details
    # Only available when the generation is finished
    details: Optional[StreamDetails] = None
    usage: Optional[Usage] = None

    def __init__(self, **kwargs: Optional[Dict[str, Any]]) -> None:
        # legacy endpoint casting
        if kwargs.get("output"):
            kwargs["choices"] = typing.cast(Dict[str, Any], kwargs["output"])["choices"]
        super().__init__(**kwargs)
