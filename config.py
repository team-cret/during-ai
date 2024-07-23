from pydantic_settings import BaseSettings, SettingsConfigDict

class ConfigSettings(BaseSettings):
    openai_api_key: str
    huggingface_api_key: str

    model_config = SettingsConfigDict(
        env_file='default.env',
        env_file_encoding='utf-8',
    )