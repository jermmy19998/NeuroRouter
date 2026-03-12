from functools import lru_cache

from fastapi import APIRouter, Depends, File, Form, UploadFile

from neurorouter.api.schemas import ClassificationResponse, InputMeta, OutputMeta, RuntimeMeta
from neurorouter.application.service import ImageClassificationService
from neurorouter.bootstrap import build_classification_service
from neurorouter.core.config import get_settings

router = APIRouter(prefix="/api/v1", tags=["inference"])


@lru_cache(maxsize=1)
def get_classification_service() -> ImageClassificationService:
    return build_classification_service()


@router.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@router.post("/classify", response_model=ClassificationResponse)
async def classify_image(
    image: UploadFile = File(...),
    instruction: str | None = Form(default=None),
    model: str | None = Form(default=None),
    top_k: int = Form(default=5),
    service: ImageClassificationService = Depends(get_classification_service),
) -> ClassificationResponse:
    image_bytes = await image.read()
    result = service.classify(
        image_bytes=image_bytes,
        instruction=instruction,
        explicit_model=model,
        top_k=top_k,
    )
    return ClassificationResponse(
        request_id=result.request_id,
        input=InputMeta(
            instruction=instruction,
            requested_model=model,
            resolved_model=result.model_alias,
            filename=image.filename or "unknown",
            content_type=image.content_type,
        ),
        output=OutputMeta(
            task=result.task,
            predictions=[
                {"label": item.label, "score": item.score} for item in result.predictions
            ],
        ),
        meta=RuntimeMeta(
            engine_source=result.engine_source,
            duration_ms=result.duration_ms,
            available_models=service.available_models(),
            timestamp=result.timestamp,
        ),
    )
