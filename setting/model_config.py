from enum import Enum

class ModelConfig(Enum):
    GEMINI_EMBEDDING_MODEL = 'models/embedding-001'
    KO_SROBERTA_EMBEDDING_MODEL = 'jhgan/ko-sroberta-multitask'
    UPSTAGE_EMBEDDING_MODEL = 'solar-embedding-1-large'
    GEMINI_LLM_MODEL = 'gemini-pro'
    LLAMA_LLM_MODEL = ''