from __future__ import annotations

from enum import Enum
from typing import List, Literal

from pydantic import StrictBool, Field, validator, field_validator

from together.types.abstract import BaseModel
from together.types.common import (
    ObjectType,
)


class FinetuneJobStatus(str, Enum):
    """
    Possible fine-tune job status
    """

    STATUS_PENDING = "pending"
    STATUS_QUEUED = "queued"
    STATUS_RUNNING = "running"
    STATUS_COMPRESSING = "compressing"
    STATUS_UPLOADING = "uploading"
    STATUS_CANCEL_REQUESTED = "cancel_requested"
    STATUS_CANCELLED = "cancelled"
    STATUS_ERROR = "error"
    STATUS_USER_ERROR = "user_error"
    STATUS_COMPLETED = "completed"


class FinetuneEventLevels(str, Enum):
    """
    Fine-tune job event status levels
    """

    NULL = ""
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"
    LEGACY_INFO = "info"
    LEGACY_IWARNING = "warning"
    LEGACY_IERROR = "error"


class FinetuneEventType(str, Enum):
    """
    Fine-tune job event types
    """

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
    EVAL_COMPLETE = "EVAL_COMPLETE"
    TRAINING_COMPLETE = "TRAINING_COMPLETE"
    MODEL_COMPRESSING = "COMPRESSING_MODEL"
    MODEL_COMPRESSION_COMPLETE = "MODEL_COMPRESSION_COMPLETE"
    MODEL_UPLOADING = "MODEL_UPLOADING"
    MODEL_UPLOAD_COMPLETE = "MODEL_UPLOAD_COMPLETE"
    JOB_COMPLETE = "JOB_COMPLETE"
    JOB_ERROR = "JOB_ERROR"
    JOB_USER_ERROR = "JOB_USER_ERROR"
    CANCEL_REQUESTED = "CANCEL_REQUESTED"
    JOB_RESTARTED = "JOB_RESTARTED"
    REFUND = "REFUND"
    WARNING = "WARNING"


class DownloadCheckpointType(Enum):
    DEFAULT = "default"
    MERGED = "merged"
    ADAPTER = "adapter"


class FinetuneEvent(BaseModel):
    """
    Fine-tune event type
    """

    # object type
    object: Literal[ObjectType.FinetuneEvent]
    # created at datetime stamp
    created_at: str | None = None
    # event log level
    level: FinetuneEventLevels | None = None
    # event message string
    message: str | None = None
    # event type
    type: FinetuneEventType | None = None
    # optional: model parameter count
    param_count: int | None = None
    # optional: dataset token count
    token_count: int | None = None
    # optional: weights & biases url
    wandb_url: str | None = None
    # event hash
    hash: str | None = None


class TrainingType(BaseModel):
    """
    Abstract training type
    """

    type: str


class FullTrainingType(TrainingType):
    """
    Training type for full fine-tuning
    """

    type: str = "Full"


class LoRATrainingType(TrainingType):
    """
    Training type for LoRA adapters training
    """

    lora_r: int
    lora_alpha: int
    lora_dropout: float = 0.0
    lora_trainable_modules: str = "all-linear"
    type: str = "Lora"


class TrainingMethod(BaseModel):
    """
    Training method type
    """

    method: str


class TrainingMethodSFT(TrainingMethod):
    """
    Training method type for SFT training
    """

    method: Literal["sft"] = "sft"


class TrainingMethodDPO(TrainingMethod):
    """
    Training method type for DPO training
    """

    method: Literal["dpo"] = "dpo"
    dpo_beta: float | None = None


class FinetuneRequest(BaseModel):
    """
    Fine-tune request type
    """

    # training file ID
    training_file: str
    # validation file id
    validation_file: str | None = None
    # base model string
    model: str
    # number of epochs to train for
    n_epochs: int
    # training learning rate
    learning_rate: float
    # learning rate scheduler type and args
    lr_scheduler: FinetuneLRScheduler | None = None
    # learning rate warmup ratio
    warmup_ratio: float
    # max gradient norm
    max_grad_norm: float
    # weight decay
    weight_decay: float
    # number of checkpoints to save
    n_checkpoints: int | None = None
    # number of evaluation loops to run
    n_evals: int | None = None
    # training batch size
    batch_size: int | None = None
    # up to 40 character suffix for output model name
    suffix: str | None = None
    # weights & biases api key
    wandb_key: str | None = None
    # weights & biases base url
    wandb_base_url: str | None = None
    # wandb project name
    wandb_project_name: str | None = None
    # wandb run name
    wandb_name: str | None = None
    # training type
    training_type: FullTrainingType | LoRATrainingType | None = None
    # train on inputs
    train_on_inputs: StrictBool | Literal["auto"] = "auto"
    # training method
    training_method: TrainingMethodSFT | TrainingMethodDPO = Field(
        default_factory=TrainingMethodSFT
    )
    # from step
    from_checkpoint: str | None = None


class FinetuneResponse(BaseModel):
    """
    Fine-tune API response type
    """

    # job ID
    id: str | None = None
    # training file id
    training_file: str | None = None
    # validation file id
    validation_file: str | None = None
    # base model name
    model: str | None = None
    # output model name
    output_name: str | None = Field(None, alias="model_output_name")
    # adapter output name
    adapter_output_name: str | None = None
    # number of epochs
    n_epochs: int | None = None
    # number of checkpoints to save
    n_checkpoints: int | None = None
    # number of evaluation loops
    n_evals: int | None = None
    # training batch size
    batch_size: int | None = None
    # training learning rate
    learning_rate: float | None = None
    # learning rate scheduler type and args
    lr_scheduler: FinetuneLRScheduler | None = None
    # learning rate warmup ratio
    warmup_ratio: float | None = None
    # max gradient norm
    max_grad_norm: float | None = None
    # weight decay
    weight_decay: float | None = None
    # number of steps between evals
    eval_steps: int | None = None
    # training type
    training_type: TrainingType | None = None
    # created/updated datetime stamps
    created_at: str | None = None
    updated_at: str | None = None
    # job status
    status: FinetuneJobStatus | None = None
    # job id
    job_id: str | None = None
    # list of fine-tune events
    events: List[FinetuneEvent] | None = None
    # dataset token count
    token_count: int | None = None
    # model parameter count
    param_count: int | None = None
    # fine-tune job price
    total_price: int | None = None
    # total number of training steps
    total_steps: int | None = None
    # number of steps completed (incrementing counter)
    steps_completed: int | None = None
    # number of epochs completed (incrementing counter)
    epochs_completed: int | None = None
    # number of evaluation loops completed (incrementing counter)
    evals_completed: int | None = None
    # place in job queue (decrementing counter)
    queue_depth: int | None = None
    # weights & biases base url
    wandb_base_url: str | None = None
    # wandb project name
    wandb_project_name: str | None = None
    # wandb run name
    wandb_name: str | None = None
    # weights & biases job url
    wandb_url: str | None = None
    # training file metadata
    training_file_num_lines: int | None = Field(None, alias="TrainingFileNumLines")
    training_file_size: int | None = Field(None, alias="TrainingFileSize")
    train_on_inputs: StrictBool | Literal["auto"] | None = "auto"
    from_checkpoint: str | None = None

    @field_validator("training_type")
    @classmethod
    def validate_training_type(cls, v: TrainingType) -> TrainingType:
        if v.type == "Full" or v.type == "":
            return FullTrainingType(**v.model_dump())
        elif v.type == "Lora":
            return LoRATrainingType(**v.model_dump())
        else:
            raise ValueError("Unknown training type")


class FinetuneList(BaseModel):
    # object type
    object: Literal["list"] | None = None
    # list of fine-tune job objects
    data: List[FinetuneResponse] | None = None


class FinetuneListEvents(BaseModel):
    # object type
    object: Literal["list"] | None = None
    # list of fine-tune events
    data: List[FinetuneEvent] | None = None


class FinetuneDownloadResult(BaseModel):
    # object type
    object: Literal["local"] | None = None
    # fine-tune job id
    id: str | None = None
    # checkpoint step number
    checkpoint_step: int | None = None
    # local path filename
    filename: str | None = None
    # size in bytes
    size: int | None = None


class FinetuneFullTrainingLimits(BaseModel):
    max_batch_size: int
    min_batch_size: int


class FinetuneLoraTrainingLimits(FinetuneFullTrainingLimits):
    max_rank: int
    target_modules: List[str]


class FinetuneTrainingLimits(BaseModel):
    max_num_epochs: int
    max_learning_rate: float
    min_learning_rate: float
    full_training: FinetuneFullTrainingLimits | None = None
    lora_training: FinetuneLoraTrainingLimits | None = None


class FinetuneLRScheduler(BaseModel):
    lr_scheduler_type: str
    lr_scheduler_args: FinetuneLinearLRSchedulerArgs | None = None


class FinetuneLinearLRSchedulerArgs(BaseModel):
    min_lr_ratio: float | None = 0.0


class FinetuneCheckpoint(BaseModel):
    """
    Fine-tuning checkpoint information
    """

    # checkpoint type (e.g. "Intermediate", "Final", "Final Merged", "Final Adapter")
    type: str
    # timestamp when the checkpoint was created
    timestamp: str
    # checkpoint name/identifier
    name: str
