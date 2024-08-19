from ai_model.embedding.text_embedding import TextEmbedding

from model.ai_model import AIModelInfo

from setting.config import Config

import google.generativeai as genai
import os

class GeminiTextEmbedding(TextEmbedding):
    def __init__(self, model_info:AIModelInfo) -> None:
        '''
            It needs ai_model_name like 'models/embedding-xxx'
        '''
        self.set_google_configuration()
        self.set_model(model_info.ai_model_name)
    
    def set_google_configuration(self) -> None:
        genai.configure(api_key=os.environ[Config.GOOGLE_API_KEY.value])

    def set_model(self, model_name:str) -> None:
        self.model_name = model_name
        
    def embed_text(self, text:str) -> list[float]:
        return genai.embed_content(
            model=self.model_name,
            content=text,
        )['embedding']