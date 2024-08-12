from enum import Enum

class ServiceConfig(Enum):
    # SENTIMENT ANALYSIS
    #-------------------------------------------------------------------------------------------#
    CURRENT_SENTIMENT_ANALYZER = 'sentiment_analyzer_v0'
    CURRENT_SENTIMENT_ANALYZER_CLASS = 'SentimentAnalyzerV0'

    SENTIMENT_ANALYZER_V0_TYPE = 'embedding'
    SENTIMENT_ANALYZER_V0_MODEL_NAME = 'upstage'
    SENTIMENT_ANALYZER_V0_CLASS_NAME = 'UpstageTextEmbedding'
    SENTIMENT_ANALYZER_V0_AI_MODEL_NAME = 'solar-embedding-1-large'
    #-------------------------------------------------------------------------------------------#


    # GOMDU CHAT
    #-------------------------------------------------------------------------------------------#
    GOMDU_CHAT_MEMORY_SIZE = 10
    GOMDU_CHAT_LLM_MODEL = 'gemini'
    GOMDU_CHAT_LLM_CLASS = 'GeminiTextGenerator'
    GOMDU_CHAT_EMBEDDING_MODEL = 'gemini'
    GOMDU_CHAT_EMBEDDING_CLASS = 'GeminiTextEmbedding'
    GOMDU_CHAT_EMBEDDING_MODEL_NAME = 'models/text-embedding-004'
    #-------------------------------------------------------------------------------------------#


    # REPORT
    #-------------------------------------------------------------------------------------------#
    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60
    #-------------------------------------------------------------------------------------------#
