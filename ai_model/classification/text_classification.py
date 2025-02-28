from abc import ABC, abstractmethod

class TextClassification(ABC):
    @abstractmethod
    def set_model(self) -> None:
        pass

    @abstractmethod
    def classify_text(self, text:str) -> dict:
        pass