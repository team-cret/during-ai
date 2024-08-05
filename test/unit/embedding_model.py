from setting.config import Config
from setting.model_config import ModelConfig
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

    def test(self):
        for model in self.embedding_models:
            vector = model.embed_text(self.text)
            print(len(vector), end=' : ')
            print(*vector[:3])