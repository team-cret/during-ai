from enum import Enum

class Config(Enum):
    GOOGLE_API_KEY = 'GOOGLE_API_KEY'
    OPENAI_API_KEY = 'OPENAI_API_KEY'
    UPSTAGE_API_KEY = 'UPSTAGE_API_KEY'
    HF_TOKEN = 'HF_TOKEN'
    ENV_FILE = 'default.env'
    ENCODING_TYPE = 'utf-8'