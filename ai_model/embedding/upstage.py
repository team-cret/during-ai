from langchain_upstage import UpstageEmbeddings

from ai_model.embedding.embedding import Embedding
from setting.model_config import ModelConfig

class UpstageTextEmbedding(Embedding):
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        self.embed_model = UpstageEmbeddings(model=ModelConfig.UPSTAGE_EMBEDDING_MODEL_NAME.value)
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)