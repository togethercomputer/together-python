from __future__ import annotations

from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import Field

from together.types.abstract import BaseModel


class BatchJobStatus(str, Enum):
    """
    The status of a batch job
    """

    VALIDATING = "VALIDATING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    CANCELING = "CANCELING"


class BatchEndpoint(str, Enum):
    """
    The endpoint of a batch job
    """

    COMPLETIONS = "/v1/completions"
    CHAT_COMPLETIONS = "/v1/chat/completions"
    # More endpoints can be added here as needed


class BatchJob(BaseModel):
    """
    A batch job object
    """

    id: str
    user_id: str
    input_file_id: str
    file_size_bytes: int
    status: BatchJobStatus
    job_deadline: datetime
    created_at: datetime
    endpoint: str
    progress: float = 0.0
    model_id: Optional[str] = None
    output_file_id: Optional[str] = None
    error_file_id: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None
