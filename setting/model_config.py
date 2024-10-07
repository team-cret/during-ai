from enum import Enum

class ModelConfig(Enum):
    # Embedding Model
    #---------------------------------------------------------------------------#
    GEMINI_EMBEDDING_MODEL_NAME = 'models/text-embedding-004'
    KO_SROBERTA_EMBEDDING_MODEL_NAME = 'jhgan/ko-sroberta-multitask'
    UPSTAGE_EMBEDDING_MODEL_NAME = 'solar-embedding-1-large'
    #---------------------------------------------------------------------------#

    # Classification Model
    #---------------------------------------------------------------------------#
    BART_LARGE_MNLI_CLASSIFICATION_MODEL = 'facebook/bart-large-mnli'
    MDEBERTA_XNLI_CLASSIFICATION_MODEL = 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'
    PONGJIN_ROBERTA_CLASSIFICATION_MODEL = 'pongjin/roberta_with_kornli'
    CLASSIFICATION_MODEL_DEVICE = -1 # 0 <=: gpu, -1: cpu
    #---------------------------------------------------------------------------#

    # Reranker Model
    #---------------------------------------------------------------------------#
    BGE_RERANKER_V2_M3_MODEL = 'BAAI/bge-reranker-v2-m3'
    GTE_RERANKER_BASE_MODEL = 'Alibaba-NLP/gte-multilingual-reranker-base'
    #---------------------------------------------------------------------------#
    
    # LLM Mode
    #---------------------------------------------------------------------------#
    GEMINI_LLM_MODEL = 'gemini-pro'
    LLAMA_LLM_MODEL = ''
    OPENAI_LLM_MODEL = 'gpt-4o-mini'
    #---------------------------------------------------------------------------#