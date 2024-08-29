import os

import google.generativeai as genai

from ai_model.embedding.embedding import Embedding
from setting.config import Config
from setting.model_config import ModelConfig

class GeminiTextEmbedding(Embedding):
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        genai.configure(api_key=os.environ[Config.GOOGLE_API_KEY.value])
        
    def embed_text(self, text:str) -> list[float]:
        return genai.embed_content(
            model=ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value,
            content=text,
        )['embedding']