from text_embedding import TextEmbedding
from langchain_openai import OpenAIEmbeddings

class OpenAITextEmbedding(TextEmbedding):
    def __init__(self) -> None:
        self.embed_model = OpenAIEmbeddings()
    
    def embed_text(self, text:str) -> list[float]:
        return self.embed_model.embed_query(text)