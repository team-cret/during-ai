from enum import Enum

from setting.model_config import ModelConfig

class ServiceConfig(Enum):
    # MOTION ANALYSIS
    #-------------------------------------------------------------------------------------------#
    CURRENT_MOTION_ANALYZER_MODULE = 'motion_analyzer_v0'
    CURRENT_MOTION_ANALYZER_CLASS = 'MotionAnalyzerV0'

    MOTION_ANALYZER_V0_TYPE = 'classification'
    MOTION_ANALYZER_V0_MODULE = 'pogjin_roberta'
    MOTION_ANALYZER_V0_CLASS = 'PongjinRobertaTextClassification'
    MOTION_ANALYZER_V0_AI_MODEL_NAME = ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value

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
    #-------------------------------------------------------------------------------------------#


    # REPORT
    #-------------------------------------------------------------------------------------------#
    REPORT_RESPONSE_TIME_ZONE_UNIT = 60
    REPORT_CONCURRENT_TIME_ZONE_UNIT = 60
    #-------------------------------------------------------------------------------------------#
