from enum import Enum

class ModelConfig(Enum):
    GEMINI_EMBEDDING_MODEL_ID = 'models/text-multilingual-embedding-002'
    GEMINI_EMBEDDING_MODEL_NAME = 'models/text-embedding-004'
    KO_SROBERTA_EMBEDDING_MODEL_NAME = 'jhgan/ko-sroberta-multitask'
    UPSTAGE_EMBEDDING_MODEL_NAME = 'solar-embedding-1-large'

    BART_LARGE_MNLI_CLASSIFICATION_MODEL = 'facebook/bart-large-mnli'
    
    GEMINI_LLM_MODEL = 'gemini-pro'
    LLAMA_LLM_MODEL = ''