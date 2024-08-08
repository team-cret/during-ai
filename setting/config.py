from enum import Enum

class Config(Enum):
    GOOGLE_PROJECT_ID = 402205469404
    GOOGLE_API_KEY = 'GOOGLE_API_KEY'
    OPENAI_API_KEY = 'OPENAI_API_KEY'
    UPSTAGE_API_KEY = 'UPSTAGE_API_KEY'
    HF_TOKEN = 'HF_TOKEN'
    ENV_FILE = 'setting/default.env'
    ENCODING_TYPE = 'utf-8'