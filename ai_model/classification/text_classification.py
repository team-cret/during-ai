from abc import ABC, abstractmethod

class TextClassification(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def classify_text(self, test:str) -> dict:
        pass