from .config import Config

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class APIKeySetting(BaseSettings):
    openai_api_key      : str
    huggingface_api_key : str
    upstage_api_key     : str
    google_api_key      : str

    model_config = SettingsConfigDict(
        env_file=Config.ENV_FILE.value,
        env_file_encoding=Config.ENCODING_TYPE.value,
    )

    def set_api_key(self):
        os.environ[Config.HF_TOKEN.value]        = self.huggingface_api_key
        os.environ[Config.OPENAI_API_KEY.value]  = self.openai_api_key
        os.environ[Config.UPSTAGE_API_KEY.value] = self.upstage_api_key
        os.environ[Config.GOOGLE_API_KEY.value]  = self.google_api_key