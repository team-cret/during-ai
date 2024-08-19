from ai_model.embedding.text_embedding import TextEmbedding

from model.ai_model import AIModelInfo

from langchain_openai import OpenAIEmbeddings

class OpenAITextEmbedding(TextEmbedding):
    def __init__(self, model_info:AIModelInfo) -> None:
        self.embed_model = OpenAIEmbeddings()
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)