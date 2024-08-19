from .text_classification import TextClassification

from data import sentiments

from model.ai_model import AIModelInfo

from setting.model_config import ModelConfig

from transformers import pipeline

class MDeBertaXnliTextClassification(TextClassification):
    def __init__(self, model_info:AIModelInfo) -> None:
        '''
            It doens't need any AI mdoel information
        '''
        self.sentiments = [value['sentiment'] for value in sentiments.sentiments.values()]
        
        self.classifier = pipeline(
            model=ModelConfig.MDEBERTA_XNLI_CLASSIFICATION_MODEL.value,
            device=0,
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