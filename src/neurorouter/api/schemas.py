from datetime import datetime

from pydantic import BaseModel, Field


class PredictionItem(BaseModel):
    label: str
    score: float = Field(ge=0, le=1)


class InputMeta(BaseModel):
    instruction: str | None = None
    requested_model: str | None = None
    resolved_model: str
    filename: str
    content_type: str | None = None


class OutputMeta(BaseModel):
    task: str
    predictions: list[PredictionItem]


class RuntimeMeta(BaseModel):
    engine_source: str
    duration_ms: int = Field(ge=0)
    available_models: list[str]
    timestamp: datetime


class ClassificationResponse(BaseModel):
    request_id: str
    input: InputMeta
    output: OutputMeta
    meta: RuntimeMeta


class ErrorResponse(BaseModel):
    error_code: str
    message: str
