from ai_model.classification.text_classification import TextClassification
from ai_model.classification.bart_large_mnli import BartLargeMnliTextClassification
from ai_model.classification.mdeberta_xnli import MDeBertaXnliTextClassification
from ai_model.classification.pogjin_roberta import PongjinRobertaTextClassification

from model.ai_model import AIModelInfo

from time import time

class ClassificationModelTester:
    def __init__(self) -> None:
        self.setup_for_test()
        self.setup_test_contents()

    def setup_for_test(self) -> None:
        self.classification_models = {
            'bart_large_mnli' : BartLargeMnliTextClassification(AIModelInfo()),
            'mdeberta_xnli' : MDeBertaXnliTextClassification(AIModelInfo()),
            'pongjin_roberta' : PongjinRobertaTextClassification(AIModelInfo()),
        }
    
    def setup_test_contents(self) -> None:
        self.test_contents = [
            {'contents_type' : 'text', 'content' : '오늘도 화이팅 하구 와요!'},
            {'contents_type' : 'text', 'content' : '오늘은 너무 피곤해'},
            {'contents_type' : 'text', 'content' : '사랑해'},
            {'contents_type' : 'text', 'content' : ''},
        ]

    def test(self):
        for model_name, model in self.classification_models.items():
            print(f'{'-' * 10}[{model_name}] classification test {'-' * (30 - len(model_name))}')
            model: TextClassification

            for test_content in self.test_contents:
                time_start = time()
                if test_content['contents_type'] == 'text':
                    result = model.classify_text(test_content['content'])
                    print(f'{test_content['content']} -> {result['sentiments'][0]}')
                print(f'elapsed time : {time() - time_start:.2f} sec')
