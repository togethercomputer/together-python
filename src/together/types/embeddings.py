from typing import List, Literal

from together.types._abstract import BaseModel

from together.types.common import (
    ObjectType,
)


class EmbeddingRequest(BaseModel):
    input: str | List[str]
    model: str


class EmbeddingChoicesData(BaseModel):
    index: int
    object: ObjectType
    embedding: List[float] | None = None


class EmbeddingResponse(BaseModel):
    id: str | None = None
    model: str | None = None
    object: Literal["list"] | None = None
    data: List[EmbeddingChoicesData] | None = None
