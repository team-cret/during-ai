from langchain_openai import OpenAIEmbeddings

from ai_model.embedding.embedding import Embedding

class OpenAITextEmbedding(Embedding):
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        self.embed_model = OpenAIEmbeddings()

    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)