from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class EvaluationType(str, Enum):
    CLASSIFY = "classify"
    SCORE = "score"
    COMPARE = "compare"


class EvaluationStatus(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    USER_ERROR = "user_error"


class JudgeModelConfig(BaseModel):
    model: str
    model_source: Literal["serverless", "dedicated", "external"]
    system_template: str
    external_api_token: Optional[str] = None
    external_base_url: Optional[str] = None


class ModelRequest(BaseModel):
    model: str
    model_source: Literal["serverless", "dedicated", "external"]
    max_tokens: int
    temperature: float
    system_template: str
    input_template: str
    external_api_token: Optional[str] = None
    external_base_url: Optional[str] = None


class ClassifyParameters(BaseModel):
    judge: JudgeModelConfig
    labels: List[str]
    pass_labels: List[str]
    model_to_evaluate: Optional[Union[str, ModelRequest]] = None
    input_data_file_path: str


class ScoreParameters(BaseModel):
    judge: JudgeModelConfig
    min_score: float
    max_score: float
    pass_threshold: float
    model_to_evaluate: Optional[Union[str, ModelRequest]] = None
    input_data_file_path: str


class CompareParameters(BaseModel):
    judge: JudgeModelConfig
    model_a: Optional[Union[str, ModelRequest]] = None
    model_b: Optional[Union[str, ModelRequest]] = None
    input_data_file_path: str


class EvaluationRequest(BaseModel):
    type: EvaluationType
    parameters: Union[ClassifyParameters, ScoreParameters, CompareParameters]


class EvaluationCreateResponse(BaseModel):
    workflow_id: str
    status: EvaluationStatus


class EvaluationJob(BaseModel):
    workflow_id: str = Field(alias="workflow_id")
    type: Optional[EvaluationType] = None
    status: EvaluationStatus
    results: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        populate_by_name = True


class EvaluationStatusResponse(BaseModel):
    status: EvaluationStatus
    results: Optional[Dict[str, Any]] = None
