from .text_embedding import TextEmbedding
from langchain_openai import OpenAIEmbeddings
from model.ai_model import AIModelInfo

class OpenAITextEmbedding(TextEmbedding):
    def __init__(self, model_info:AIModelInfo) -> None:
        self.embed_model = OpenAIEmbeddings()
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)