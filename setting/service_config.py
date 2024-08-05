from enum import Enum

class ServiceConfig(Enum):
    CURRENT_SENTIMENT_ANALYZER = 'analyzer_v0'
    SENTIMENT_ANALYZER_V0_TYPE = 'classification'
    SENTIMENT_ANALYZER_V0_MODEL_NAME = 'bart_large_mnli'
    SENTIMENT_ANALYZER_V0_CLASS_NAME = 'BartLargeMnliTextClassification'