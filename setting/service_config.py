from enum import Enum

from sqlalchemy.dialects.postgresql import UUID

from setting.model_config import ModelConfig

class ServiceConfig(Enum):
    # MOTION ANALYSIS
    #-------------------------------------------------------------------------------------------#
    CURRENT_MOTION_ANALYZER_MODULE = 'motion_analyzer_v0_1'
    CURRENT_MOTION_ANALYZER_CLASS = 'MotionAnalyzerV01'

    MOTION_ANALYZER_V0_TYPE = 'classification'
    MOTION_ANALYZER_V0_MODULE = 'pogjin_roberta'
    MOTION_ANALYZER_V0_CLASS = 'PongjinRobertaTextClassification'

    MOTION_ANALYZER_V0_1_TYPE = 'classification'
    MOTION_ANALYZER_V0_1_MODULE = 'pogjin_roberta'
    MOTION_ANALYZER_V0_1_CLASS = 'PongjinRobertaTextClassification'

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
    GOMDU_CHAT_TTL = 7200
    GOMDU_CHAT_USER_ID_LENGTH = 4

    GOMDU_CHAT_EMBEDDING_MODULE = 'ko_e5'
    GOMDU_CHAT_EMBEDDING_CLASS = 'KoE5TextEmbedding'
    # GOMDU_CHAT_EMBEDDING_MODULE = 'ko_sroberta'
    # GOMDU_CHAT_EMBEDDING_CLASS = 'KoSrobertaTextEmbedding'
    # GOMDU_CHAT_EMBEDDING_MODULE = 'openai'
    # GOMDU_CHAT_EMBEDDING_CLASS = 'OpenAITextEmbedding'
    GOMDU_CHAT_EMBEDDING_DIMENSION = 1024

    DB_TEST_COUPLE_ID_2 = ''
    DB_TEST_USER_ID_3 = ''
    DB_TEST_USER_ID_4 = ''

    DB_TEST_COUPLE_ID_3 = ''
    DB_TEST_USER_ID_5 = ''
    DB_TEST_USER_ID_6 = ''

    GOMDU_CHAT_STREAM_MODE = False
    GOMDU_CHAT_USER_NAME = 0
    GOMDU_CHAT_AI_NAME = 1
    GOMDU_CHAT_SYSTEM_NAME = 'system'

    GOMDU_CHAT_RERANKER_MODULE = 'jina_reranker_v2_base'
    GOMDU_CHAT_RERANKER_CLASS = 'JinaRerankerV2Base'
    DB_RETRIEVAL_TOP_K = 30
    RERANKER_TOP_K = 10
    #-------------------------------------------------------------------------------------------#

    # DB
    #-------------------------------------------------------------------------------------------#
    DB_CONNECTION_LOGIN = 'LOGIN'
    DB_CONNECTION_LOGOUT = 'LOGOUT'
    DB_COUPLE_STATE_CONNECTED = 'CONNECT'
    DB_CURRENT_TYPE = 'test'
    DB_DEV_SCHEMA_NAME = 'public'
    DB_LIVE_SCHEMA_NAME = 'public'
    DB_RETRIEVAL_TABLE_NAME = 'chunk_koe5'

    DB_TEST_SCHEMA_NAME = 'vectordbp'
    DB_TEST_COUPLE_ID = '5701de9e-f3b4-4fdf-8c42-e9e6965cb514'
    DB_TEST_USER_ID_1 = '9c4cf30a-fe60-495a-a21a-741b5010264f'
    DB_TEST_USER_ID_2 = '6b8338b6-abb2-423d-b572-b2b5abaf11bc'
    DB_TEST_HISTORY_ID = 846264338
    #-------------------------------------------------------------------------------------------#

    # S3
    #-------------------------------------------------------------------------------------------#
    S3_BUCKET_NAME = 'team-cret-during-s3'
    #-------------------------------------------------------------------------------------------#

    # REPORT
    #-------------------------------------------------------------------------------------------#
    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60
    REPORT_TYPE_1 = 'SMALL'
    REPORT_TYPE_2 = 'BIG'
    #-------------------------------------------------------------------------------------------#

    # BASIC
    #-------------------------------------------------------------------------------------------#
    CHAT_TYPE_MOTION = 'interaction'
    #-------------------------------------------------------------------------------------------#