from .text_embedding import TextEmbedding
from langchain_upstage import UpstageEmbeddings
import os
from model.ai_model import AIModelInfo

class UpstageTextEmbedding(TextEmbedding):
    def __init__(self, model_info:AIModelInfo) -> None:
        self.embed_model = UpstageEmbeddings(model=model_info.ai_model_name)
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)