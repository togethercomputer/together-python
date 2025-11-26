from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Literal, Optional

from together.types.abstract import BaseModel
from together.types.common import ObjectType


class ModelType(str, Enum):
    CHAT = "chat"
    LANGUAGE = "language"
    CODE = "code"
    IMAGE = "image"
    EMBEDDING = "embedding"
    MODERATION = "moderation"
    RERANK = "rerank"
    AUDIO = "audio"
    TRANSCRIBE = "transcribe"
    VIDEO = "video"


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
    # pretty name
    display_name: str | None = None
    # model creator organization
    organization: str | None = None
    # link to model resource
    link: str | None = None
    license: str | None = None
    context_length: int | None = None
    pricing: PricingObject


class ModelUploadRequest(BaseModel):
    model_name: str
    model_source: str
    model_type: Literal["model", "adapter"] = "model"
    hf_token: Optional[str] = None
    description: Optional[str] = None
    base_model: Optional[str] = None
    lora_model: Optional[str] = None


class ModelUploadResponse(BaseModel):
    job_id: Optional[str] = None
    model_name: Optional[str] = None
    model_id: Optional[str] = None
    model_source: Optional[str] = None
    message: str

    @classmethod
    def from_api_response(cls, response_data: Dict[str, Any]) -> "ModelUploadResponse":
        """Create ModelUploadResponse from API response, handling both flat and nested structures"""
        # Start with the base response
        result: Dict[str, Any] = {"message": response_data.get("message", "")}

        # Check if we have nested data
        if "data" in response_data and response_data["data"] is not None:
            # Use nested data values
            nested_data = response_data["data"]
            result.update(
                {
                    "job_id": nested_data.get("job_id"),
                    "model_name": nested_data.get("model_name"),
                    "model_id": nested_data.get("model_id"),
                    "model_source": nested_data.get("model_source"),
                }
            )
        else:
            # Use top-level values
            result.update(
                {
                    "job_id": response_data.get("job_id"),
                    "model_name": response_data.get("model_name"),
                    "model_id": response_data.get("model_id"),
                    "model_source": response_data.get("model_source"),
                }
            )

        return cls(**result)
