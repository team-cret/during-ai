from setting.config import Config
from setting.model_config import ModelConfig
from model.ai_model import AIModelInfo
from ai_model.embedding import (
    gemini,
    ko_sroberta,
    openai,
    upstage,
)

class EmbeddingModelTester:
    def __init__(self) -> None:
        self.test_text = '이것은 테스트 텍스트 입니다'
        self.setup_for_test()

    def setup_for_test(self) -> None:
        self.embedding_models = [
            gemini.GeminiTextEmbedding(AIModelInfo(
                api_key_name=Config.GOOGLE_API_KEY.value,
                ai_model_id=ModelConfig.GEMINI_EMBEDDING_MODEL_ID.value,
                ai_model_name=ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value
            )),
            ko_sroberta.KoSrobertaTextEmbedding(AIModelInfo(
                    ai_model_name=ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value
            )),
            openai.OpenAITextEmbedding(AIModelInfo()),
            upstage.UpstageTextEmbedding(AIModelInfo(
                    ai_model_name=ModelConfig.UPSTAGE_EMBEDDING_MODEL_NAME.value
            ),),
        ]

    def test(self):
        for model in self.embedding_models:
            vector = model.embed_text(self.test_text)
            print(len(vector), end=' : ')
            print(*vector[:3])