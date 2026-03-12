from io import BytesIO
from threading import Lock

from PIL import Image, UnidentifiedImageError

from neurorouter.domain.entities import Prediction
from neurorouter.domain.errors import InferenceEngineError, InvalidInputError
from neurorouter.domain.ports import ImageClassifierPort


class HuggingFaceImageClassifier(ImageClassifierPort):
    """Thread-safe lazy wrapper for Hugging Face image classification pipeline."""

    def __init__(self, hf_model_id: str) -> None:
        self._hf_model_id = hf_model_id
        self._pipeline = None
        self._lock = Lock()

    def _get_pipeline(self):
        if self._pipeline is not None:
            return self._pipeline

        with self._lock:
            if self._pipeline is not None:
                return self._pipeline
            try:
                from transformers import pipeline
            except Exception as exc:  # pragma: no cover - import error is environment specific
                raise InferenceEngineError(
                    "transformers dependency is missing or broken."
                ) from exc

            try:
                self._pipeline = pipeline(
                    task="image-classification",
                    model=self._hf_model_id,
                )
            except Exception as exc:
                raise InferenceEngineError(
                    f"Failed to initialize model '{self._hf_model_id}'."
                ) from exc
            return self._pipeline

    def classify(self, image_bytes: bytes, top_k: int) -> list[Prediction]:
        try:
            image = Image.open(BytesIO(image_bytes)).convert("RGB")
        except UnidentifiedImageError as exc:
            raise InvalidInputError("Uploaded file is not a valid image.") from exc
        except Exception as exc:
            raise InvalidInputError("Failed to read uploaded image file.") from exc

        model_pipeline = self._get_pipeline()
        try:
            raw_predictions = model_pipeline(image, top_k=top_k)
        except Exception as exc:
            raise InferenceEngineError("Model inference failed.") from exc

        return [
            Prediction(
                label=str(item.get("label", "")),
                score=float(item.get("score", 0.0)),
            )
            for item in raw_predictions
        ]

