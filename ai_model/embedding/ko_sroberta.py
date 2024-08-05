from text_embedding import TextEmbedding
from langchain_huggingface import HuggingFaceEmbeddings
import os

class KoSrobertaTextEmbedding(TextEmbedding):
    def __init__(self, model_name:str) -> None:
        self.embed_model = HuggingFaceEmbeddings(
            model_name=model_name
        )
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)