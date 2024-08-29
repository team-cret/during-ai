from transformers import pipeline

from ai_model.classification.text_classification import TextClassification
from data.motions import motions
from setting.model_config import ModelConfig

class MDeBertaXnliTextClassification(TextClassification):
    def __init__(self) -> None:
        self.set_model()

    def set_model(self) -> None:
        self.motions = [value['motion'] for value in motions.values()]
        
        self.classifier = pipeline(
            model=ModelConfig.MDEBERTA_XNLI_CLASSIFICATION_MODEL.value,
            device=-1,
        )

    def classify_text(self, text:str) -> dict:
        result = self.classifier(
            text,
            candidate_labels=self.motions,
            multi_label=True
        )
        
        return {
            'motions' : result['labels'],
            'scores' : result['scores']
        }