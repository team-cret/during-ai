from ai_model.embedding.gemini import GeminiTextEmbedding
from ai_model.embedding.ko_sroberta import KoSrobertaTextEmbedding
from ai_model.embedding.openai import OpenAITextEmbedding
from ai_model.embedding.embedding import Embedding
from ai_model.embedding.upstage import UpstageTextEmbedding
from ai_model.embedding.int_float import IntFloatTextEmbedding
from ai_model.embedding.jina_embedding_v3 import JinaEmbeddingV3TextEmbedding

class EmbeddingModelTester:
    def __init__(self) -> None:
        self.setup_for_test()
        self.setup_test_contents()

    def setup_for_test(self) -> None:
        self.embedding_models = {
            'gemini' : GeminiTextEmbedding(),
            'ko_sroberta' : KoSrobertaTextEmbedding(),
            # 'upstage' : UpstageTextEmbedding(),
            'openai' : OpenAITextEmbedding(),
            # 'intfloat' : IntFloatTextEmbedding(),
            'jina-embedding-v3' : JinaEmbeddingV3TextEmbedding(),
        }
    
    def setup_test_contents(self) -> None:
        self.test_contents = [
            {'contents_type' : 'text', 'content' : '이것은 테스트 텍스트 입니다'},
        ]

    def test(self):
        for model_name, model in self.embedding_models.items():
            model: Embedding

            for test_content in self.test_contents:
                if test_content['contents_type'] == 'text':
                    vector = model.embed_text(test_content['content'])
                    print(f'[{model_name} text embedding] -', len(vector), end=' : ')
                    print(*vector[:1])