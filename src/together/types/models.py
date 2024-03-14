from __future__ import annotations

from typing import List, Literal

from enum import Enum

from together.types.abstract import BaseModel
from together.types.common import ObjectType


class ModelType(str, Enum):
    CHAT = "chat"
    LANGUAGE = "language"
    CODE = "code"
    IMAGE = "image"
    EMBEDDING = "embedding"
    MODERATION = "moderation"


class PricingObject(BaseModel):
    input: float | None = None
    output: float | None = None
    hourly: float | None = None
    base: float | None = None
    finetune: float | None = None


class ModelObject(BaseModel):
    # model id
    id: str
    # object type
    object: Literal[ObjectType.Model]
    created: int | None = None
    # model type
    type: ModelType | None = None
    # model creator organization
    organization: str | None = None
    # link to model resource
    link: str | None = None
    license: str | None = None
    pricing: PricingObject | None = None
