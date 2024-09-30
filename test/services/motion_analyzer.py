from model.data_model import CoupleChat

from tabulate import tabulate

from data.motions import motions, motion_to_id
from data.motion_analysis_data import data
from model.data_model import Motion
from service.motion_analysis.motion_analyzer_v0 import MotionAnalyzerV0
from service.motion_analysis.motion_analyzer_v0_1 import MotionAnalyzerV01
from service.motion_analysis.motion_analyzer_v1 import  MotionAnalyzerV1
from service.motion_analysis.motion_analyzer import MotionAnalyzer

from time import time

class MotionAnalyzerTester:
    def __init__(self) -> None:
        self.setup_for_test()
        self.setup_test_contents()
    
    def setup_for_test(self):
        self.sentiment_analyzers = {
            # 'motion_analyzerV0' : MotionAnalyzerV0(),
            'motion_analyzerV01' : MotionAnalyzerV01(),
            # 'motion_analyzerV1' : MotionAnalyzerV1(),
        }

    def setup_test_contents(self):
        self.test_contents = data
    
    def test(self):
        for analyzer_name, analyzer in self.sentiment_analyzers.items():
            print(f'[{analyzer_name}] sentiment analyzer test')
            analyzer: MotionAnalyzer

            score = 0
            nnone = 0
            failure = 0
            type_information = {
                0 : {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0},
                1 : {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0},
                2 : {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0},
                3 : {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0},
                4 : {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0},
                5 : {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0},
            }
            type_name = {
                0 : 'general',
                1 : 'mixed',
                2 : 'cute tone',
                3 : 'space, punctuation',
                4 : 'honorfics',
                5 : 'difficult',
            }

            motion_information = {}
            motion_name = {}
            for motion, value in motions.items():
                motion_information[motion] = {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0}
                motion_name[motion] = value['motion']
            motion_information[9999] = {'score' : 0, 'nnone' : 0, 'num' : 0, 'failure' : 0}
            motion_name[9999] = '없음'

            failure_cases = []
            for test_content in self.test_contents:
                start_time  = time()
                if test_content['contents_type'] == 'text':
                    analyzed_motion:Motion = analyzer.analyze_motion(
                        CoupleChat(message=test_content['content'])
                    )
                    end_time = time()
                    print(f'[elapsed time : {end_time - start_time:.2f} sec] : ' + 
                          f'{test_content['content']} -> {analyzed_motion.motion}')
                    if analyzed_motion.motion == test_content['label']:
                        score += 1
                        type_information[test_content['type']]['score'] += 1
                        motion_information[motion_to_id[test_content['label']]]['score'] += 1
                    if analyzed_motion.motion == '없음':
                        nnone += 1
                        type_information[test_content['type']]['nnone'] += 1
                        motion_information[motion_to_id[test_content['label']]]['nnone'] += 1
                    elif analyzed_motion.motion != test_content['label']:
                        failure += 1
                        type_information[test_content['type']]['failure'] += 1
                        motion_information[motion_to_id[test_content['label']]]['failure'] += 1

                        failure_cases.append({
                            'content' : test_content['content'],
                            'label' : test_content['label'],
                            'motion' : analyzed_motion.motion,
                        })
                    type_information[test_content['type']]['num'] += 1
                    motion_information[motion_to_id[test_content['label']]]['num'] += 1
            
            headers = ['type_name', 'failure', 'none_num', 'accuracy']
            analyzer_result_by_type = [
                [
                    'total', 
                    f"{failure / len(self.test_contents) * 100:.2f}%",
                    f"{nnone / len(self.test_contents) * 100:.2f}%",
                    f"{score / len(self.test_contents) * 100:.2f}%",
                ]
            ]
            for type_num, type_info in type_information.items():
                analyzer_result_by_type.append([
                    type_name[type_num],
                    f"{type_info['failure'] / type_info['num'] * 100:.2f}%",
                    f"{type_info['nnone'] / type_info['num'] * 100:.2f}%",
                    f"{type_info['score'] / type_info['num'] * 100:.2f}%",
                ])
            table = tabulate(analyzer_result_by_type, headers=headers, tablefmt='grid')
            print(table)

            analyzer_result_by_motion = []
            for motion_id, motion_info in motion_information.items():
                analyzer_result_by_motion.append([
                    motion_name[motion_id],
                    f"{motion_info['failure'] / motion_info['num'] * 100:.2f}%",
                    f"{motion_info['nnone'] / motion_info['num'] * 100:.2f}%",
                    f"{motion_info['score'] / motion_info['num'] * 100:.2f}%",
                ])
            table = tabulate(analyzer_result_by_motion, headers=headers, tablefmt='grid')
            print(table)

            for failure_case in failure_cases:
                print(failure_case)