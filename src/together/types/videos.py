from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from together.types.abstract import BaseModel


class CreateVideoBody(BaseModel):
    """Request model for video creation"""

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
    output_format: Literal["MP4", "WEBM"] | None = (
        None  # "MP4" or "WEBM", default "MP4"
    )
    output_quality: int | None = None  # Compression quality, default 20
    negative_prompt: str | None = None

    # Advanced parameters
    frame_images: List[Dict[str, Any]] | None = None  # Array of keyframe images
    reference_images: List[str] | None = None  # Array of reference images


class VideoOutputs(BaseModel):
    """Response from video creation request"""

    cost: float
    video_url: str


class VideoInfoError(BaseModel):
    """Error about the video creation request"""

    code: str
    message: str


class VideoInfo(BaseModel):
    """Info about the video creation request"""

    user_id: str
    errors: List[VideoInfoError] | None = None


class CreateVideoResponse(BaseModel):
    """Response from video generation request"""

    id: str


class VideoResource(BaseModel):
    """Response from video status check"""

    id: str
    model: str
    status: Literal["queued", "in_progress", "completed", "failed", "cancelled"]
    info: VideoInfo | None = None
    inputs: Dict[str, Any]
    outputs: VideoOutputs | None = None
    created_at: str
    claimed_at: str
    done_at: str
