from ai_model.embedding.text_embedding import TextEmbedding

from langchain_huggingface import HuggingFaceEmbeddings

import os
from model.ai_model import AIModelInfo

class KoSrobertaTextEmbedding(TextEmbedding):
    def __init__(self, model_info:AIModelInfo) -> None:
        self.embed_model = HuggingFaceEmbeddings(
            model_name=model_info.ai_model_name,
        )
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)