class NeuroRouterError(Exception):
    """Base exception for domain and application errors."""


class ModelNotFoundError(NeuroRouterError):
    def __init__(self, model_alias: str) -> None:
        super().__init__(f"Model alias '{model_alias}' is not registered.")
        self.model_alias = model_alias


class InvalidInputError(NeuroRouterError):
    """Raised when user input or files are invalid."""


class InferenceEngineError(NeuroRouterError):
    """Raised when model runtime cannot process an inference request."""

