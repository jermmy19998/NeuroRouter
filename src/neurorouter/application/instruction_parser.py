import re


class InstructionModelResolver:
    """Resolve model aliases from a user instruction with typo tolerance."""

    _resnet18_patterns = (
        r"\bresnet[-_\s]?18\b",
        r"\brenet[-_\s]?18\b",
        r"\brenet\b",
        r"\bresnet\b",
        r"resnet18",
        r"renet18",
    )

    def resolve(self, instruction: str | None, explicit_model: str | None, default_model: str) -> str:
        if explicit_model and explicit_model.strip():
            return explicit_model.strip().lower()

        text = (instruction or "").strip().lower()
        if not text:
            return default_model

        if any(re.search(pattern, text) for pattern in self._resnet18_patterns):
            return "resnet18"

        return default_model

