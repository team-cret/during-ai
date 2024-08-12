from ai_model.embedding.gemini import GeminiTextEmbedding
from ai_model.embedding.ko_sroberta import KoSrobertaTextEmbedding
from ai_model.embedding.openai import OpenAITextEmbedding
from ai_model.embedding.text_embedding import TextEmbedding
from ai_model.embedding.upstage import UpstageTextEmbedding

from setting.model_config import ModelConfig

from model.ai_model import AIModelInfo

class EmbeddingModelTester:
    def __init__(self) -> None:
        self.setup_for_test()
        self.setup_test_contents()

    def setup_for_test(self) -> None:
        self.embedding_models = {
            'gemini' : GeminiTextEmbedding(AIModelInfo(
                ai_model_name=ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value
            )),
            'ko_sroberta' : KoSrobertaTextEmbedding(AIModelInfo(
                ai_model_name=ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value
            )),
            'upstage' : UpstageTextEmbedding(AIModelInfo(
                ai_model_name=ModelConfig.UPSTAGE_EMBEDDING_MODEL_NAME.value
            )),
            'openai' : OpenAITextEmbedding(AIModelInfo()),
        }
    
    def setup_test_contents(self) -> None:
        self.test_contents = [
            {'contents_type' : 'text', 'content' : '이것은 테스트 텍스트 입니다'},
        ]

    def test(self):
        for model_name, model in self.embedding_models.items():
            model: TextEmbedding

            for test_content in self.test_contents:
                if test_content['contents_type'] == 'text':
                    vector = model.embed_text(test_content['content'])
                    print(f'[{model_name} text embedding] -', len(vector), end=' : ')
                    print(*vector[:1])