import json
from collections.abc import Callable
from pathlib import Path

from neurorouter.domain.errors import ModelNotFoundError
from neurorouter.domain.ports import ImageClassifierPort
from neurorouter.infrastructure.hf_classifier import HuggingFaceImageClassifier

ModelFactory = Callable[[], ImageClassifierPort]


class ModelRegistry:
    """Register and lazily instantiate model adapters by alias."""

    def __init__(self) -> None:
        self._factories: dict[str, ModelFactory] = {}
        self._instances: dict[str, ImageClassifierPort] = {}
        self._sources: dict[str, str] = {}

    def register(self, alias: str, source: str, factory: ModelFactory) -> None:
        normalized = alias.strip().lower()
        self._factories[normalized] = factory
        self._sources[normalized] = source

    def get(self, alias: str) -> ImageClassifierPort:
        normalized = alias.strip().lower()
        if normalized not in self._factories:
            raise ModelNotFoundError(normalized)
        if normalized not in self._instances:
            self._instances[normalized] = self._factories[normalized]()
        return self._instances[normalized]

    def source(self, alias: str) -> str:
        normalized = alias.strip().lower()
        return self._sources.get(normalized, "unknown")

    def available_models(self) -> list[str]:
        return sorted(self._factories.keys())


def build_default_model_registry(custom_model_map_file: str | None = None) -> ModelRegistry:
    registry = ModelRegistry()
    registry.register(
        alias="resnet18",
        source="huggingface:microsoft/resnet-18",
        factory=lambda: HuggingFaceImageClassifier("microsoft/resnet-18"),
    )
    registry.register(
        alias="resnet-18",
        source="huggingface:microsoft/resnet-18",
        factory=lambda: HuggingFaceImageClassifier("microsoft/resnet-18"),
    )

    if custom_model_map_file:
        _register_custom_models(registry, custom_model_map_file)
    return registry


def _register_custom_models(registry: ModelRegistry, custom_model_map_file: str) -> None:
    file_path = Path(custom_model_map_file)
    if not file_path.exists():
        return

    payload = json.loads(file_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return

    for alias, source in payload.items():
        if not isinstance(alias, str) or not isinstance(source, str):
            continue
        if not source.startswith("hf:"):
            continue
        hf_model_id = source.removeprefix("hf:").strip()
        if not hf_model_id:
            continue
        registry.register(
            alias=alias,
            source=f"huggingface:{hf_model_id}",
            factory=lambda model_id=hf_model_id: HuggingFaceImageClassifier(model_id),
        )

