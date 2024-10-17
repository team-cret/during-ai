from langchain_huggingface import HuggingFaceEmbeddings
import logging

from ai_model.embedding.embedding import Embedding
from setting.model_config import ModelConfig
from setting.logger_setting import logger_setting

class KoSrobertaTextEmbedding(Embedding):
    def __init__(self) -> None:
        self.set_model()
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_model(self) -> None:
        self.embed_model = HuggingFaceEmbeddings(
            model_name=ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value,
        )
    
    def embed_text(self, text:str) -> list[float]:
        try:
            return self.embed_model.embed_query(text)
        except Exception as e:
            self.logger.error(f"Error in embedding text (ko_sroberta): {str(e)}", exc_info=True)
            raise Exception("Error in embedding text")
    
    def embed_text_list(self, text_list:list[str]) -> list[list[float]]:
        try:
            return self.embed_model.embed_documents(text_list)
        except Exception as e:
            self.logger.error(f"Error in embedding text list (ko_sroberta): {str(e)}", exc_info=True)
            raise Exception("Error in embedding text list")