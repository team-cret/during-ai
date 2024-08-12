from setting.model_config import ModelConfig

from enum import Enum

class ServiceConfig(Enum):
    # SENTIMENT ANALYSIS
    #-------------------------------------------------------------------------------------------#
    CURRENT_SENTIMENT_ANALYZER_MODULE = 'sentiment_analyzer_v0'
    CURRENT_SENTIMENT_ANALYZER_CLASS = 'SentimentAnalyzerV0'

    SENTIMENT_ANALYZER_V0_TYPE = 'embedding'
    SENTIMENT_ANALYZER_V0_MODULE = 'ko_sroberta'
    SENTIMENT_ANALYZER_V0_CLASS = 'KoSrobertaTextEmbedding'
    SENTIMENT_ANALYZER_V0_AI_MODEL_NAME = ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value
    #-------------------------------------------------------------------------------------------#


    # GOMDU CHAT
    #-------------------------------------------------------------------------------------------#
    GOMDU_CHAT_MEMORY_SIZE = 10
    GOMDU_CHAT_LLM_MODULE = 'gemini'
    GOMDU_CHAT_LLM_CLASS = 'GeminiTextGenerator'
    GOMDU_CHAT_EMBEDDING_MODULE = 'gemini'
    GOMDU_CHAT_EMBEDDING_CLASS = 'GeminiTextEmbedding'
    GOMDU_CHAT_EMBEDDING_MODEL_NAME = ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value
    #-------------------------------------------------------------------------------------------#


    # REPORT
    #-------------------------------------------------------------------------------------------#
    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60
    #-------------------------------------------------------------------------------------------#
