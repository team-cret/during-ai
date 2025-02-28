from abc import ABC, abstractmethod

from PIL import Image

class Embedding:
    @abstractmethod
    def set_model(self) -> None:
        pass

    def embed_text(self, test:str) -> list[float]:
        pass

    def embed_image(self, image:Image) -> list[float]:
        pass