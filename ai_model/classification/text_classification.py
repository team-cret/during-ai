from abc import ABC, abstractmethod

class TextClassification(ABC):
    @abstractmethod
    def classify_text(self, test:str) -> dict:
        pass