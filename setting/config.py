from enum import Enum

class Config(Enum):
    # Key Configuration
    #------------------------------------------------#
    GOOGLE_PROJECT_ID = 402205469404
    GOOGLE_API_KEY = 'GOOGLE_API_KEY'
    OPENAI_API_KEY = 'OPENAI_API_KEY'
    UPSTAGE_API_KEY = 'UPSTAGE_API_KEY'
    HF_TOKEN = 'HF_TOKEN'
    ENCRYPTOR_KEY = 'ENCRYPTOR_KEY'
    AWS_ACCESS_KEY = 'AWS_ACCESS_KEY'
    AWS_SECRET_KEY = 'AWS_SECRET_KEY'

    # Key Value File
    #------------------------------------------------#
    ENV_FILE = 'setting/default.env'
    ENCODING_TYPE = 'utf-8'
    #------------------------------------------------#