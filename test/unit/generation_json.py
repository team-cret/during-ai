
from ai_model.generation.generation import Generation
from ai_model.generation.openai import OpenAITextGenerator
from model.data_model import CoupleChat

class GenerationJsonTester:
    def __init__(self):
        self.setup_for_test()
        self.setup_test_contents()
    
    def setup_for_test(self):
        self.model = [
            OpenAITextGenerator()
        ]
    
    def setup_test_contents(self):
        self.test_contents = [
            '이것은 테스트 데이터 입니다.'
        ]

    def test(self):
        for model in self.model:
            model: Generation

            for content in self.test_contents:
                result = model.analyze_motion(CoupleChat(message=content))

            print(result)
