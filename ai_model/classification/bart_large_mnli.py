from .text_classification import TextClassification
from setting.model_config import ModelConfig
from data import sentiments
from transformers import pipeline

class BartLargeMnliTextClassification(TextClassification):
    def __init__(self) -> None:
        self.sentiments = sentiments.sentiments
        self.classifier = pipeline(
            model=ModelConfig.BART_LARGE_MNLI_CLASSIFICATION_MODEL.value,
            device_map='auto',
        )

    def classify_text(self, message:str) -> tuple[str, str]:
        result = self.classifier(
            message,
            candidate_labels=self.sentiments,
            multi_label=True
        )
        
        return {
            'sentiments' : result['labels'],
            'scores' : result['scores']
        }
