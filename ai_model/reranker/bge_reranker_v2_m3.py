from FlagEmbedding import FlagReranker

from ai_model.reranker.reranker import Reranker
from model.data_model import RetrievedData
from setting.model_config import ModelConfig

class BgeRerankerV2M3(Reranker):
    def __init__(self) -> None:
        self.set_model()

    def set_model(self) -> None:
        self.reranker = FlagReranker(
            ModelConfig.BGE_RERANKER_V2_M3_MODEL.value,
            use_fp16=True
        )

    def rerank_documents(self, documents:list[RetrievedData], query:str) -> tuple[list[RetrievedData], list[float]]:
        scores = self.reranker.compute_score([[query, document.original_message] for document in documents])

        return [documents[i] for i in sorted(range(len(documents)), key=lambda x:scores[x], reverse=True)], sorted(scores)