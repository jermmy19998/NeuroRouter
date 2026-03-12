from abc import ABC, abstractmethod

from neurorouter.domain.entities import Prediction


class ImageClassifierPort(ABC):
    @abstractmethod
    def classify(self, image_bytes: bytes, top_k: int) -> list[Prediction]:
        raise NotImplementedError

