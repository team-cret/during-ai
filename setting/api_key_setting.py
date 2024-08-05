from pydantic_settings import BaseSettings, SettingsConfigDict
from config import Config
import os

class APIKeySetting(BaseSettings):
    openai_api_key: str
    huggingface_api_key: str
    upstage_api_key: str
    google_api_key: str

    model_config = SettingsConfigDict(
        env_file=Config.ENV_FILE,
        env_file_encoding=Config.ENCODING_TYPE,
    )

    def setAPIKeys(self):
        os.environ[Config.HF_TOKEN] = self.huggingface_api_key
        os.environ[Config.OPENAI_API_KEY] = self.openai_api_key
        os.environ[Config.UPSTAGE_API_KEY] = self.upstage_api_key
        os.environ[Config.GOOGLE_API_KEY] = self.google_api_key

