from langchain_huggingface import HuggingFaceEmbeddings

from ai_model.embedding.embedding import Embedding
from setting.model_config import ModelConfig

class KoSrobertaTextEmbedding(Embedding):
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        self.embed_model = HuggingFaceEmbeddings(
            model_name=ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value,
        )
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)