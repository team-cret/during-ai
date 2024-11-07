import logging

from transformers import AutoModelForSequenceClassification

from setting.logger_setting import logger_setting
from model.data_model import RetrievedData

class JinaRerankerV2Base:
    def __init__(self) -> None:
        self.set_model()
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_model(self) -> None:
        self.reranker = AutoModelForSequenceClassification.from_pretrained(
            'jinaai/jina-reranker-v2-base-multilingual',
            torch_dtype="auto",
            trust_remote_code=True,
        )

        self.reranker.to('cpu')
        self.reranker.eval()
    
    def rerank_documents(self, documents:list[RetrievedData], query:str) -> list[RetrievedData]:
        try:
            scores = self.reranker.compute_score(
                [[query, document.original_message] for document in documents]
            )
            
            return [documents[i] for i in sorted(range(len(documents)), key=lambda x:scores[x], reverse=True)]
        except Exception as e:
            self.logger.error(f"Error in reranking documents: {str(e)}", exc_info=True)
            raise Exception("Error in reranking documents")