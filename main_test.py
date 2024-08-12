from setting import init_setting

class Tester:
    def __init__(self) -> None:
        init_setting.init_setting()
        self.setup_for_test()
    
    def setup_for_test(self):
        # unit test
        #---------------------------------------------------------------------------#
        from test.unit.embedding_model import EmbeddingModelTester
        print('success import EmbeddingModelTester')
        from test.unit.classification_model import ClassificationModelTester
        print('success import ClassificationModelTester')
        #---------------------------------------------------------------------------#

        # service test
        #---------------------------------------------------------------------------#
        from test.services.sentiment_analyzer import SentimentAnalyzerTester
        print('success import SentimentAnalyzerTester')
        from test.services.gomdu_chat_generator import GomduChatGeneratorTester
        print('success import GomduChatGeneratorTester')
        from test.services.report_generator import ReportGeneratorTester
        print('success import ReportGeneratorTester')
        #---------------------------------------------------------------------------#
        
        # select targeted test [True <-> False]
        #---------------------------------------------------------------------------#
        self.test_setup = {
            'embedding_model'      : [False, EmbeddingModelTester()],
            'classification_model' : [True, ClassificationModelTester()],
            'sentiment_analysis'   : [False, SentimentAnalyzerTester()],
            'chat_generator'       : [False, GomduChatGeneratorTester()],
            'report_generator'     : [False, ReportGeneratorTester()],
        }
        print('successfully end setup for test')
        #---------------------------------------------------------------------------#

    def test(self):
        for task, TF_tester in self.test_setup.items():
            TF, tester = TF_tester
            
            print('current task:', task, '-' * (50-len(task)))
            if TF:
                tester.test()

tester = Tester()
tester.test()