import pytest

from neurorouter.application.instruction_parser import InstructionModelResolver
from neurorouter.application.service import ImageClassificationService
from neurorouter.domain.entities import Prediction
from neurorouter.domain.errors import InvalidInputError, ModelNotFoundError
from neurorouter.infrastructure.registry import ModelRegistry


class FakeClassifier:
    def classify(self, image_bytes: bytes, top_k: int) -> list[Prediction]:
        assert image_bytes
        return [
            Prediction(label="tabby, tabby cat", score=0.91),
            Prediction(label="tiger cat", score=0.05),
        ][:top_k]


def _make_service() -> ImageClassificationService:
    registry = ModelRegistry()
    registry.register("resnet18", "fake:resnet18", lambda: FakeClassifier())
    return ImageClassificationService(
        model_registry=registry,
        instruction_model_resolver=InstructionModelResolver(),
        default_model_alias="resnet18",
        max_upload_bytes=1000,
    )


def test_classify_returns_structured_result() -> None:
    service = _make_service()
    result = service.classify(
        image_bytes=b"fake-image",
        instruction="help me use resnet",
        explicit_model=None,
        top_k=2,
    )
    assert result.task == "image_classification"
    assert result.model_alias == "resnet18"
    assert len(result.predictions) == 2


def test_classify_validates_empty_file() -> None:
    service = _make_service()
    with pytest.raises(InvalidInputError):
        service.classify(
            image_bytes=b"",
            instruction=None,
            explicit_model=None,
            top_k=1,
        )


def test_classify_validates_unknown_model() -> None:
    service = _make_service()
    with pytest.raises(ModelNotFoundError):
        service.classify(
            image_bytes=b"fake-image",
            instruction=None,
            explicit_model="missing-model",
            top_k=1,
        )

