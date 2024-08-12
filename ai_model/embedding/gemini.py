from .text_embedding import TextEmbedding

from model.ai_model import AIModelInfo

from setting.config import Config

import google.generativeai as genai
import os

class GeminiTextEmbedding(TextEmbedding):
    def __init__(self, model_info:AIModelInfo) -> None:
        '''
            need ai_model_name like 'models/embedding-xxx'
        '''
        genai.configure(api_key=os.environ[Config.GOOGLE_API_KEY.value])
        self._model_name = model_info.ai_model_name
        # vertexai.init(project=Config.GOOGLE_PROJECT_ID.value)
        # self.embedding_model = TextEmbeddingModel.from_pretrained(model_info.ai_model_id)
        
    def embed_text(self, text:str) -> list[float]:
        # return self.embedding_model.get_embeddings(text)
        return genai.embed_content(
            model=self._model_name,
            content=text,
        )['embedding']