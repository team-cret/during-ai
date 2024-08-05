from text_embedding import TextEmbedding
import google.generativeai as genai
import os

class GeminiTextEmbedding(TextEmbedding):
    def __init__(self, model_name:str, api_key_name) -> None:
        genai.configure(api_key=os.environ[api_key_name])
        self._model_name = model_name
    
    def embed_text(self, text:str) -> list[float]:
        return genai.embed_content(
            model=self._model_name,
            content=text,
        )['embedding']