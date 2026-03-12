from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Prediction:
    label: str
    score: float


@dataclass(slots=True, frozen=True)
class InferenceResult:
    request_id: str
    task: str
    model_alias: str
    engine_source: str
    predictions: list[Prediction]
    duration_ms: int
    timestamp: datetime
