from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class ConfigSettings(BaseSettings):
    openai_api_key: str
    huggingface_api_key: str
    upstage_api_key: str

    model_config = SettingsConfigDict(
        env_file='default.env',
        env_file_encoding='utf-8',
    )

    def setAPIKeys(self):
        os.environ['HF_TOKEN'] = self.huggingface_api_key
        os.environ['OPENAI_API_KEY'] = self.openai_api_key
        os.environ['UPSTAGE_API_KEY'] = self.upstage_api_key
