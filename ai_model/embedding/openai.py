from langchain_openai import OpenAIEmbeddings
import logging

from ai_model.embedding.embedding import Embedding
from setting.logger_setting import logger_setting

class OpenAITextEmbedding(Embedding):
    def __init__(self) -> None:
        self.set_model()
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_model(self) -> None:
        self.embed_model = OpenAIEmbeddings()

    def embed_text(self, text:str) -> list[float]:
        try:
            return self.embed_model.embed_query(text)
        except Exception as e:
            self.logger.error(f"Error in embedding text (openai): {str(e)}", exc_info=True)
            raise Exception("Error in embedding text")