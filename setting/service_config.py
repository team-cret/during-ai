from enum import Enum

class ServiceConfig(Enum):
    CURRENT_SENTIMENT_ANALYZER = 'analyzer_v0'
    SENTIMENT_ANALYZER_V0_TYPE = 'classification'
    SENTIMENT_ANALYZER_V0_MODEL_NAME = 'bart_large_mnli'
    SENTIMENT_ANALYZER_V0_CLASS_NAME = 'BartLargeMnliTextClassification'

    GOMDU_CHAT_MEMORY_SIZE = 10
    GOMDU_CHAT_LLM_MODEL = 'gemini'
    GOMDU_CHAT_LLM_CLASS = 'GeminiTextGenerator'
    GOMDU_CHAT_EMBEDDING_MODEL = 'gemini'
    GOMDU_CHAT_EMBEDDING_CLASS = 'GeminiTextEmbedding'
    GOMDU_CHAT_EMBEDDING_MODEL_NAME = 'models/text-embedding-004'

    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60