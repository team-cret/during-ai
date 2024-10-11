from setting import init_setting
from time import time

class Tester:
    def __init__(self) -> None:
        init_setting.init_setting()
        self.setup_for_test()
    
    def setup_for_test(self):
        # unit test
        #---------------------------------------------------------------------------#
        time_start = time()
        from test.unit.embedding_model import EmbeddingModelTester
        print('success import EmbeddingModelTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        time_start = time()
        from test.unit.classification_model import ClassificationModelTester
        print('success import ClassificationModelTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        time_start = time()
        from test.unit.db_test import DBTester
        print('success import DBTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        time_start = time()
        from test.unit.generation_json import GenerationJsonTester
        print('success import GenerationJsonTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        #---------------------------------------------------------------------------#

        # service test
        #---------------------------------------------------------------------------#
        time_start = time()
        from test.services.motion_analyzer import MotionAnalyzerTester
        print('success import MotionAnalyzerTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        time_start = time()
        from test.services.gomdu_chat_generator import GomduChatGeneratorTester
        print('success import GomduChatGeneratorTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        time_start = time()
        from test.services.report_generator import ReportGeneratorTester
        print('success import ReportGeneratorTester' + f' [elapsed time : {time() - time_start:.2f} sec]')
        #---------------------------------------------------------------------------#
        
        # select targeted test [True <-> False]
        #---------------------------------------------------------------------------#
        time_start = time()
        self.test_setup = {
            'embedding_model'      : [True, EmbeddingModelTester()],
            # 'classification_model' : [False, ClassificationModelTester()],
            # 'db'                   : [False, DBTester()],
            # 'generation_json'      : [True, GenerationJsonTester()],

            # 'motion_analyzer'      : [True, MotionAnalyzerTester()],
            'chat_generator'       : [True, GomduChatGeneratorTester()],
            # 'report_generator'     : [False, ReportGeneratorTester()],
        }
        print('successfully end setup for test' + f'elapsed time : {time() - time_start:.2f} sec')
        #---------------------------------------------------------------------------#

    def test(self):
        for task, TF_tester in self.test_setup.items():
            TF, tester = TF_tester
            
            if TF:
                print('current task:', task, '-' * (50-len(task)))
                tester.test()

tester = Tester()
tester.test()