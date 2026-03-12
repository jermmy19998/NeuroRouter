from neurorouter.application.instruction_parser import InstructionModelResolver
from neurorouter.application.service import ImageClassificationService
from neurorouter.core.config import get_settings
from neurorouter.infrastructure.registry import build_default_model_registry


def build_classification_service() -> ImageClassificationService:
    settings = get_settings()
    registry = build_default_model_registry(settings.custom_model_map_file)
    return ImageClassificationService(
        model_registry=registry,
        instruction_model_resolver=InstructionModelResolver(),
        default_model_alias=settings.default_model_alias,
        max_upload_bytes=settings.max_upload_bytes,
    )

