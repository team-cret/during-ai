from text_embedding import TextEmbedding
from langchain_upstage import UpstageEmbeddings
import os

class UpstageTextEmbedding(TextEmbedding):
    def __init__(self, model_name:str) -> None:
        self.embed_model = UpstageEmbeddings(model=model_name)
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)