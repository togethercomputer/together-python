from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from together.types.abstract import BaseModel


class VideoRequest(BaseModel):
    """Request model for video generation"""

    # Required parameters
    model: str
    prompt: str

    # Optional dimension parameters
    height: int | None = None
    width: int | None = None

    # Optional generation parameters
    seconds: float | None = None  # Min 1 max 10
    fps: int | None = None  # Frames per second, min 15 max 60, default 24
    steps: int | None = None  # Denoising steps, min 10 max 50, default 20
    seed: int | None = None
    guidance_scale: float | None = None  # Default 8, recommended 6.0-10.0
    output_format: str | None = None  # "MP4" or "WEBM", default "MP4"
    output_quality: int | None = None  # Compression quality, default 20
    negative_prompt: str | None = None

    # Advanced parameters
    frame_images: List[Dict[str, Any]] | None = None  # Array of keyframe images
    reference_images: List[Dict[str, Any]] | None = None  # Array of reference images
    metadata: Dict[str, Any] | None = None


class VideoInputs(BaseModel):
    """Input parameters used for video generation"""

    model: str
    prompt: str
    height: int
    width: int
    seconds: float
    seed: int | None = None
    fps: int | None = None
    steps: int | None = None
    guidance_scale: float | None = None
    output_quality: int | None = None
    output_format: str | None = None
    negative_prompt: str | None = None
    frame_images: List[Dict[str, Any]] | None = None
    reference_images: List[Dict[str, Any]] | None = None
    metadata: Dict[str, Any] | None = None


class VideoOutputs(BaseModel):
    """Output information for completed video generation"""

    cost: float
    video_url: str


class VideoGenerateResponse(BaseModel):
    """Response from video generation request"""

    id: str


class VideoStatusResponse(BaseModel):
    """Response from video status check"""

    id: str
    model: str
    status: Literal["queued", "in_progress", "completed", "failed", "cancelled"]
    info: Dict[str, Any] | None = None
    inputs: VideoInputs
    outputs: VideoOutputs | None = None
    created_at: str
    claimed_at: str
    done_at: str
