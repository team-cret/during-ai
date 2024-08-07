import init_setting

class Tester:
    def __init__(self) -> None:
        init_setting.init_setting()
        self.setup_for_test()
    
    def setup_for_test(self):
        from unit.embedding_model import EmbeddingModelTester
        print('success EmbeddingModelTester')
        from unit.classification_model import ClassificationModelTester
        print('success ClassificationModelTester')
        from services.sentiment_analyzer import SentimentAnalyzerTester
        print('success SentimentAnalyzerTester')
        from services.gomdu_chat_generator import GomduChatGeneratorTester
        print('success GomduChatGeneratorTester')

        self.test_setup = {
            'embedding_model'      : [False, EmbeddingModelTester()],
            'classification_model' : [False, ClassificationModelTester()],
            'sentiment_analysis'   : [False, SentimentAnalyzerTester()],
            'chat_generator'       : [True, GomduChatGeneratorTester()],
        }
        print('successfully end setup for test')

    def test(self):
        for task, value in self.test_setup.items():
            do_test, tester = value
            print('current task:', task, '-'*(70 - len(task)))
            if do_test:
                tester.test()

tester = Tester()
tester.test()