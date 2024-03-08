from typing import List, Literal

from together.types._abstract import BaseModel, Field
from enum import Enum

from together.types.common import (
    ObjectType,
)


class FinetuneJobStatus(str, Enum):
    STATUS_PENDING = "pending"
    STATUS_QUEUED = "queued"
    STATUS_RUNNING = "running"
    STATUS_COMPRESSING = "compressing"
    STATUS_UPLOADING = "uploading"
    STATUS_CANCEL_REQUESTED = "cancel_requested"
    STATUS_CANCELLED = "cancelled"
    STATUS_ERROR = "error"
    STATUS_COMPLETED = "completed"


class FinetuneEventLevels(str, Enum):
    NULL = ""
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class FinetuneEventType(str, Enum):
    JOB_PENDING = "JOB_PENDING"
    JOB_START = "JOB_START"
    JOB_STOPPED = "JOB_STOPPED"
    MODEL_DOWNLOADING = "MODEL_DOWNLOADING"
    MODEL_DOWNLOAD_COMPLETE = "MODEL_DOWNLOAD_COMPLETE"
    TRAINING_DATA_DOWNLOADING = "TRAINING_DATA_DOWNLOADING"
    TRAINING_DATA_DOWNLOAD_COMPLETE = "TRAINING_DATA_DOWNLOAD_COMPLETE"
    VALIDATION_DATA_DOWNLOADING = "VALIDATION_DATA_DOWNLOADING"
    VALIDATION_DATA_DOWNLOAD_COMPLETE = "VALIDATION_DATA_DOWNLOAD_COMPLETE"
    WANDB_INIT = "WANDB_INIT"
    TRAINING_START = "TRAINING_START"
    CHECKPOINT_SAVE = "CHECKPOINT_SAVE"
    BILLING_LIMIT = "BILLING_LIMIT"
    EPOCH_COMPLETE = "EPOCH_COMPLETE"
    TRAINING_COMPLETE = "TRAINING_COMPLETE"
    MODEL_COMPRESSING = "COMPRESSING_MODEL"
    MODEL_COMPRESSION_COMPLETE = "MODEL_COMPRESSION_COMPLETE"
    MODEL_UPLOADING = "MODEL_UPLOADING"
    MODEL_UPLOAD_COMPLETE = "MODEL_UPLOAD_COMPLETE"
    JOB_COMPLETE = "JOB_COMPLETE"
    JOB_ERROR = "JOB_ERROR"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    JOB_RESTARTED = "JOB_RESTARTED"
    REFUND = "REFUND"
    WARNING = "WARNING"


class FinetuneEvent(BaseModel):
    object: Literal[ObjectType.FinetuneEvent]
    created_at: str | None = None
    level: FinetuneEventLevels | None = None
    message: str | None = None
    type: FinetuneEventType | None = None
    param_count: int | None = None
    token_count: int | None = None
    wandb_url: str | None = None
    hash: str | None = None


class FinetuneRequest(BaseModel):
    training_file: str
    model: str
    n_epochs: int
    learning_rate: float
    n_checkpoints: int | None = None
    batch_size: int | None = None
    suffix: str | None = None
    wandb_api_key: str | None = None


class FinetuneResponse(BaseModel):
    id: str | None = None
    training_file: str | None = None
    validation_file: str | None = None
    model: str | None = None
    modeloutput: str | None = Field(None, alias="model_output_name")
    n_epochs: int | None = None
    n_checkpoints: int | None = None
    batch_size: int | None = None
    learning_rate: float | None = None
    eval_steps: int | None = None
    lora: bool | None = None
    lora_r: int | None = None
    lora_alpha: int | None = None
    lora_dropout: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    status: FinetuneJobStatus | None = None
    job_id: str | None = None
    events: List[FinetuneEvent] | None = None
    token_count: int | None = None
    param_count: int | None = None
    total_price: int | None = None
    epochs_completed: int | None = None
    queue_depth: int | None = None
    wandb_project_name: str | None = None
    wandb_url: str | None = None
    TrainingFileNumLines: int | None = None
    TrainingFileSize: int | None = None
