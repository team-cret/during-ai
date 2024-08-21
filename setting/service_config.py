from setting.model_config import ModelConfig

from enum import Enum

class ServiceConfig(Enum):
    # SENTIMENT ANALYSIS
    #-------------------------------------------------------------------------------------------#
    CURRENT_SENTIMENT_ANALYZER_MODULE = 'sentiment_analyzer_v0'
    CURRENT_SENTIMENT_ANALYZER_CLASS = 'SentimentAnalyzerV0'

    SENTIMENT_ANALYZER_V0_TYPE = 'classification'
    SENTIMENT_ANALYZER_V0_MODULE = 'pogjin_roberta'
    SENTIMENT_ANALYZER_V0_CLASS = 'PongjinRobertaTextClassification'
    SENTIMENT_ANALYZER_V0_AI_MODEL_NAME = ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value

    SENTIMENT_ANALYZER_V1_MODULE1 = 'pogjin_roberta'
    SENTIMENT_ANALYZER_V1_CLASS1 = 'PongjinRobertaTextClassification'
    SENTIMENT_ANALYZER_V1_MODULE2 = 'mdeberta_xnli'
    SENTIMENT_ANALYZER_V1_CLASS2 = 'MDeBertaXnliTextClassification'
    SENTIMENT_ANALYZER_V1_MODULE3 = 'bart_large_mnli'
    SENTIMENT_ANALYZER_V1_CLASS3 = 'BartLargeMnliTextClassification'
    #-------------------------------------------------------------------------------------------#


    # GOMDU CHAT
    #-------------------------------------------------------------------------------------------#
    GOMDU_CHAT_MEMORY_SIZE = 10
    GOMDU_CHAT_LLM_MODULE = 'openai'
    GOMDU_CHAT_LLM_CLASS = 'OpenAITextGenerator'
    GOMDU_CHAT_EMBEDDING_MODULE = 'gemini'
    GOMDU_CHAT_EMBEDDING_CLASS = 'GeminiTextEmbedding'
    GOMDU_CHAT_EMBEDDING_MODEL_NAME = ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value
    #-------------------------------------------------------------------------------------------#


    # REPORT
    #-------------------------------------------------------------------------------------------#
    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60
    #-------------------------------------------------------------------------------------------#
