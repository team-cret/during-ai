from FlagEmbedding import FlagReranker
import logging

from ai_model.reranker.reranker import Reranker
from model.data_model import RetrievedData
from setting.model_config import ModelConfig
from setting.logger_setting import logger_setting

class BgeRerankerV2M3(Reranker):
    def __init__(self) -> None:
        self.set_model()
        logger_setting()
        self.logger = logging.getLogger(__name__)

    def set_model(self) -> None:
        self.reranker = FlagReranker(
            ModelConfig.BGE_RERANKER_V2_M3_MODEL.value,
            use_fp16=True
        )

    def rerank_documents(self, documents:list[RetrievedData], query:str) -> tuple[list[RetrievedData], list[float]]:
        try:
            scores = self.reranker.compute_score([[query, document.original_message] for document in documents])
            
            return [documents[i] for i in sorted(range(len(documents)), key=lambda x:scores[x], reverse=True)]
        except Exception as e:
            self.logger.error(f"Error in reranking documents: {str(e)}", exc_info=True)
            raise Exception("Error in reranking documents")