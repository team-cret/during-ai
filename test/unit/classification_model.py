from setting.config import Config
from setting.model_config import ModelConfig
from ai_model.classification import bart_large_mnli
from data import sentiments

class ClassificationModelTester:
    def __init__(self) -> None:
        self.text = '이것은 테스트 텍스트 입니다'
        self.setup_for_test()

    def setup_for_test(self) -> None:
        self.classification_models = [
            bart_large_mnli.BartLargeMnliTextClassification(),
        ]

    def test(self):
        print("Start Classification Model Test")
        for model in self.classification_models:
            result = model.classify_text(self.text)
            print(result)
        print("End Classification Model Test")
        print()
        
