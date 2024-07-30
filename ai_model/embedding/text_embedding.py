from abc import ABC, abstractmethod

class TextEmbedding:
    @abstractmethod
    def embed_text(self, test:str) -> list[float]:
        pass