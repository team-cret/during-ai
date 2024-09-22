from enum import Enum

from sqlalchemy.dialects.postgresql import UUID

from setting.model_config import ModelConfig

class ServiceConfig(Enum):
    # MOTION ANALYSIS
    #-------------------------------------------------------------------------------------------#
    CURRENT_MOTION_ANALYZER_MODULE = 'motion_analyzer_v0'
    CURRENT_MOTION_ANALYZER_CLASS = 'MotionAnalyzerV0'

    MOTION_ANALYZER_V0_TYPE = 'classification'
    MOTION_ANALYZER_V0_MODULE = 'pogjin_roberta'
    MOTION_ANALYZER_V0_CLASS = 'PongjinRobertaTextClassification'

    MOTION_ANALYZER_V1_MODULE1 = 'pogjin_roberta'
    MOTION_ANALYZER_V1_CLASS1 = 'PongjinRobertaTextClassification'
    MOTION_ANALYZER_V1_MODULE2 = 'mdeberta_xnli'
    MOTION_ANALYZER_V1_CLASS2 = 'MDeBertaXnliTextClassification'
    MOTION_ANALYZER_V1_MODULE3 = 'bart_large_mnli'
    MOTION_ANALYZER_V1_CLASS3 = 'BartLargeMnliTextClassification'
    #-------------------------------------------------------------------------------------------#

    # GOMDU CHAT
    #-------------------------------------------------------------------------------------------#
    GOMDU_CHAT_MEMORY_SIZE = 10
    GOMDU_CHAT_LLM_MODULE = 'openai'
    GOMDU_CHAT_LLM_CLASS = 'OpenAITextGenerator'
    GOMDU_CHAT_EMBEDDING_MODULE = 'openai'
    GOMDU_CHAT_EMBEDDING_CLASS = 'OpenAITextEmbedding'
    GOMDU_CHAT_EMBEDDING_MODEL_NAME = ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value
    GOMDU_CHAT_EMBEDDING_DIMENSION = 1536
    GOMDU_CHAT_STREAM_MODE = False
    GOMDU_CHAT_USER_NAME = 'user'
    GOMDU_CHAT_AI_NAME = 'gomdu'
    GOMDU_CHAT_SYSTEM_NAME = 'system'
    GOMDU_CHAT_RERANKER_MODULE = 'bge_reranker_v2_m3'
    GOMDU_CHAT_RERANKER_CLASS = 'BgeRerankerV2M3'

    DB_RETRIEVAL_TOP_K = 15
    RERANKER_TOP_K = 5
    #-------------------------------------------------------------------------------------------#

    # DB
    #-------------------------------------------------------------------------------------------#
    DB_CONNECTION_LOGIN = 'LOGIN'
    DB_CONNECTION_LOGOUT = 'LOGOUT'
    DB_SCHEMA_NAME = 'vectordb'
    DB_RETRIEVAL_TABLE_NAME = 'chunk'
    DB_TEST_SCHEMA_NAME = 'vectordb'
    DB_TEST_COUPLE_ID = '5701de9e-f3b4-4fdf-8c42-e9e6965cb514'
    DB_TEST_USER_ID_1 = '9c4cf30a-fe60-495a-a21a-741b5010264f'
    DB_TEST_USER_ID_2 = '6b8338b6-abb2-423d-b572-b2b5abaf11bc'
    DB_TEST_HISTORY_ID = 846264338
    #-------------------------------------------------------------------------------------------#

    # REPORT
    #-------------------------------------------------------------------------------------------#
    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60
    REPORT_TYPE_1 = 'SMALL'
    REPORT_TYPE_2 = 'BIG'
    #-------------------------------------------------------------------------------------------#
