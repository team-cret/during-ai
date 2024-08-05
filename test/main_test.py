import init_setting

class Tester:
    def __init__(self) -> None:
        init_setting.init_setting()
        self.setup_for_test()
    
    def setup_for_test(self):
        from unit.embedding_model import EmbeddingModelTester
        from unit.classification_model import ClassificationModelTester
        from services.sentiment_analyzer import SentimentAnalyzerTester

        self.test_setup = {
            'embedding_model'      : [False, EmbeddingModelTester()],
            'classification_model' : [False, ClassificationModelTester()],
            'sentiment_analysis'   : [True, SentimentAnalyzerTester()],
        }

    def test(self):
        for do_test, tester in self.test_setup.values():
            if do_test:
                tester.test()

tester = Tester()
tester.test()