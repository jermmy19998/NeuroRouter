import base64

from fastapi.testclient import TestClient

from neurorouter.application.instruction_parser import InstructionModelResolver
from neurorouter.application.service import ImageClassificationService
from neurorouter.domain.entities import Prediction
from neurorouter.infrastructure.registry import ModelRegistry
from neurorouter.main import app
from neurorouter.api.routes import get_classification_service


class FakeClassifier:
    def classify(self, image_bytes: bytes, top_k: int) -> list[Prediction]:
        return [
            Prediction(label="golden retriever", score=0.88),
            Prediction(label="Labrador retriever", score=0.08),
        ][:top_k]


def _service_override() -> ImageClassificationService:
    registry = ModelRegistry()
    registry.register("resnet18", "fake:resnet18", lambda: FakeClassifier())
    return ImageClassificationService(
        model_registry=registry,
        instruction_model_resolver=InstructionModelResolver(),
        default_model_alias="resnet18",
        max_upload_bytes=1024 * 1024,
    )


def test_classify_endpoint_returns_predictions() -> None:
    app.dependency_overrides[get_classification_service] = _service_override
    client = TestClient(app)
    image_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO0I6xQAAAAASUVORK5CYII="
    )

    response = client.post(
        "/api/v1/classify",
        files={"image": ("tiny.png", image_bytes, "image/png")},
        data={"instruction": "帮我用resnet分类这个图像", "top_k": "2"},
    )
    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["output"]["task"] == "image_classification"
    assert payload["input"]["resolved_model"] == "resnet18"
    assert len(payload["output"]["predictions"]) == 2

