from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4

from neurorouter.application.instruction_parser import InstructionModelResolver
from neurorouter.domain.entities import InferenceResult
from neurorouter.domain.errors import InvalidInputError
from neurorouter.infrastructure.registry import ModelRegistry


class ImageClassificationService:
    def __init__(
        self,
        model_registry: ModelRegistry,
        instruction_model_resolver: InstructionModelResolver,
        default_model_alias: str,
        max_upload_bytes: int,
    ) -> None:
        self._model_registry = model_registry
        self._instruction_model_resolver = instruction_model_resolver
        self._default_model_alias = default_model_alias
        self._max_upload_bytes = max_upload_bytes

    def available_models(self) -> list[str]:
        return self._model_registry.available_models()

    def classify(
        self,
        image_bytes: bytes,
        instruction: str | None,
        explicit_model: str | None,
        top_k: int,
    ) -> InferenceResult:
        if not image_bytes:
            raise InvalidInputError("Image file is empty.")
        if len(image_bytes) > self._max_upload_bytes:
            raise InvalidInputError(
                f"Image exceeds max upload size ({self._max_upload_bytes} bytes)."
            )
        if top_k < 1 or top_k > 10:
            raise InvalidInputError("top_k must be between 1 and 10.")

        model_alias = self._instruction_model_resolver.resolve(
            instruction=instruction,
            explicit_model=explicit_model,
            default_model=self._default_model_alias,
        )
        classifier = self._model_registry.get(model_alias)

        started = perf_counter()
        predictions = classifier.classify(image_bytes=image_bytes, top_k=top_k)
        duration_ms = int((perf_counter() - started) * 1000)

        return InferenceResult(
            request_id=str(uuid4()),
            task="image_classification",
            model_alias=model_alias,
            engine_source=self._model_registry.source(model_alias),
            predictions=predictions,
            duration_ms=duration_ms,
            timestamp=datetime.now(UTC),
        )
