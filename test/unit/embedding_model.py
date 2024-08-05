
import sys
import os

dir_path = os.path.abspath(os.path.dirname('during-ai'))
sys.path.insert(0, dir_path)
print(dir_path)
from setting.config import Config
from setting.model_config import ModelConfig
from setting.api_key_setting import APIKeySetting
from ai_model.embedding import (
    gemini,
    ko_sroberta,
    openai,
    upstage,
)

def test_embedding_model():
    APIKeySetting().setAPIKeys()

    embedding_models = [
        gemini.GeminiTextEmbedding(
            ModelConfig.GEMINI_EMBEDDING_MODEL.value,
            Config.GOOGLE_API_KEY.value,
        ),
        ko_sroberta.KoSrobertaTextEmbedding(
            ModelConfig.KO_SROBERTA_EMBEDDING_MODEL.value
        ),
        openai.OpenAITextEmbedding(),
        upstage.UpstageTextEmbedding(
            ModelConfig.UPSTAGE_EMBEDDING_MODEL.value
        ),
    ]

    text = '이것은 테스트 텍스트 입니다'
    for model in embedding_models:
        vector = model.embed_text(text)
        print(len(vector), end=' : ')
        print(*vector[:3])
test_embedding_model()