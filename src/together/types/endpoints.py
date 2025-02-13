from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel, Field


class TogetherJSONModel(BaseModel):
    """Base model with JSON serialization support."""

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        exclude_none = kwargs.pop("exclude_none", True)
        data = super().model_dump(exclude_none=exclude_none, **kwargs)

        # Convert datetime objects to ISO format strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()

        return data


class Autoscaling(TogetherJSONModel):
    """Configuration for automatic scaling of replicas based on demand."""

    min_replicas: int = Field(
        description="The minimum number of replicas to maintain, even when there is no load"
    )
    max_replicas: int = Field(
        description="The maximum number of replicas to scale up to under load"
    )


class EndpointPricing(TogetherJSONModel):
    """Pricing details for using an endpoint."""

    cents_per_minute: float = Field(
        description="Cost per minute of endpoint uptime in cents"
    )


class HardwareSpec(TogetherJSONModel):
    """Detailed specifications of a hardware configuration."""

    gpu_type: str = Field(description="The type/model of GPU")
    gpu_link: str = Field(description="The GPU interconnect technology")
    gpu_memory: Union[float, int] = Field(description="Amount of GPU memory in GB")
    gpu_count: int = Field(description="Number of GPUs in this configuration")


class HardwareAvailability(TogetherJSONModel):
    """Indicates the current availability status of a hardware configuration."""

    status: Literal["available", "unavailable", "insufficient"] = Field(
        description="The availability status of the hardware configuration"
    )


class HardwareWithStatus(TogetherJSONModel):
    """Hardware configuration details with optional availability status."""

    object: Literal["hardware"] = Field(description="The type of object")
    id: str = Field(description="Unique identifier for the hardware configuration")
    pricing: EndpointPricing = Field(
        description="Pricing details for this hardware configuration"
    )
    specs: HardwareSpec = Field(description="Detailed specifications of this hardware")
    availability: Optional[HardwareAvailability] = Field(
        default=None,
        description="Current availability status of this hardware configuration",
    )
    updated_at: datetime = Field(
        description="Timestamp of when the hardware status was last updated"
    )


class BaseEndpoint(TogetherJSONModel):
    """Base class for endpoint models with common fields."""

    object: Literal["endpoint"] = Field(description="The type of object")
    id: Optional[str] = Field(
        default=None, description="Unique identifier for the endpoint"
    )
    name: str = Field(description="System name for the endpoint")
    model: str = Field(description="The model deployed on this endpoint")
    type: str = Field(description="The type of endpoint")
    owner: str = Field(description="The owner of this endpoint")
    state: Literal["PENDING", "STARTING", "STARTED", "STOPPING", "STOPPED", "ERROR"] = (
        Field(description="Current state of the endpoint")
    )
    created_at: datetime = Field(description="Timestamp when the endpoint was created")


class ListEndpoint(BaseEndpoint):
    """Details about an endpoint when listed via the list endpoint."""

    type: Literal["dedicated", "serverless"] = Field(description="The type of endpoint")


class DedicatedEndpoint(BaseEndpoint):
    """Details about a dedicated endpoint deployment."""

    id: str = Field(description="Unique identifier for the endpoint")
    type: Literal["dedicated"] = Field(description="The type of endpoint")
    display_name: str = Field(description="Human-readable name for the endpoint")
    hardware: str = Field(
        description="The hardware configuration used for this endpoint"
    )
    autoscaling: Autoscaling = Field(
        description="Configuration for automatic scaling of the endpoint"
    )


__all__ = [
    "DedicatedEndpoint",
    "ListEndpoint",
    "Autoscaling",
    "EndpointPricing",
    "HardwareSpec",
    "HardwareAvailability",
    "HardwareWithStatus",
]
