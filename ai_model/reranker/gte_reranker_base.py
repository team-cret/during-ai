import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from ai_model.reranker.reranker import Reranker
from model.data_model import RetrievedData
from setting.model_config import ModelConfig

class GteRerankerBase(Reranker):
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(ModelConfig.GTE_RERANKER_BASE_MODEL.value)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            ModelConfig.GTE_RERANKER_BASE_MODEL.value,
            trust_remote_code=True,
            torch_dtype=torch.float16
        )
    
    def rerank_documents(self, documents:list[RetrievedData], query:str) -> list[RetrievedData]:
        inputs = self.tokenizer(
            [query] * len(documents),
            [document.original_message for document in documents],
            padding=True,
            truncation=True,
            return_tensors='pt'
        )
        outputs = self.model(**inputs)
        scores = outputs.logits.squeeze().tolist()

        return [documents[i] for i in sorted(range(len(documents)), key=lambda x:scores[x], reverse=True)], sorted(scores)