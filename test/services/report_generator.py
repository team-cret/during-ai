from datetime import datetime
from time import time

from model.data_model import ReportRequest
from service.report.report_generator import ReportGenerator
from setting.service_config import ServiceConfig

class ReportGeneratorTester:
    def __init__(self): 
        self.setup_for_test()
        self.setup_test_contents()

    def setup_for_test(self):
        # self.couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value
        # self.couple_id = ServiceConfig.DB_TEST_COUPLE_ID_2.value
        self.couple_id = ServiceConfig.DB_TEST_COUPLE_ID_3.value

    def setup_test_contents(self):
        self.test_contents = [
            # 태희
            # {'start' : datetime(2022, 1, 10), 'end' : datetime(2022, 2, 1)},
            # {'start' : datetime(2022, 1, 1), 'end' : datetime(2022, 1, 6)},
            # {'start' : datetime(2022, 2, 1), 'end' : datetime(2022, 2, 6)},
            # {'start' : datetime(2022, 3, 1), 'end' : datetime(2022, 3, 6)},
            # {'start' : datetime(2022, 4, 1), 'end' : datetime(2022, 4, 6)},
            # {'start' : datetime(2022, 5, 1), 'end' : datetime(2022, 5, 6)},
            # {'start' : datetime(2022, 6, 1), 'end' : datetime(2022, 6, 6)},
            # {'start' : datetime(2022, 7, 1), 'end' : datetime(2022, 7, 6)},
            # {'start' : datetime(2022, 8, 1), 'end' : datetime(2022, 8, 6)},
            # {'start' : datetime(2022, 9, 1), 'end' : datetime(2022, 9, 6)},
            # {'start' : datetime(2022, 10, 1), 'end' : datetime(2022, 10, 6)},
            # {'start' : datetime(2022, 11, 1), 'end' : datetime(2022, 11, 6)},
            # {'start' : datetime(2022, 12, 1), 'end' : datetime(2022, 12, 6)},
            # {'start' : datetime(2022, 12, 21), 'end' : datetime(2022, 12, 27)},

            # 유진
            # {'start' : datetime(2022, 11, 1), 'end' : datetime(2022, 11, 30)},
            # {'start' : datetime(2023, 1, 1), 'end' : datetime(2023, 3, 1)},
            # {'start' : datetime(2023, 5, 1), 'end' : datetime(2023, 5, 30)},

            # {'start' : datetime(2022, 11, 1), 'end' : datetime(2022, 11, 5)},
            # {'start' : datetime(2022, 12, 25), 'end' : datetime(2022, 12, 30)},
            # {'start' : datetime(2023, 2, 20), 'end' : datetime(2023, 2, 25)},

            # 세린
            {'start' : datetime(2023, 11, 1), 'end' : datetime(2023, 11, 30)},
            {'start' : datetime(2024, 1, 1), 'end' : datetime(2024, 3, 1)},
            {'start' : datetime(2024, 5, 1), 'end' : datetime(2024, 5, 30)},

            {'start' : datetime(2023, 11, 1), 'end' : datetime(2023, 11, 5)},
            {'start' : datetime(2023, 12, 25), 'end' : datetime(2023, 12, 30)},
            {'start' : datetime(2024, 2, 20), 'end' : datetime(2024, 2, 25)},
        ]

    def test(self):
        for content in self.test_contents:
            start_time = time()
            report_generator = ReportGenerator(
                ReportRequest(
                    couple_id=self.couple_id,
                    start_date=content['start'],
                    end_date=content['end'],
                    couple_member_ids=[
                        # ServiceConfig.DB_TEST_USER_ID_1.value,
                        # ServiceConfig.DB_TEST_USER_ID_2.value,
                        # ServiceConfig.DB_TEST_USER_ID_3.value,
                        # ServiceConfig.DB_TEST_USER_ID_4.value,
                        ServiceConfig.DB_TEST_USER_ID_5.value,
                        ServiceConfig.DB_TEST_USER_ID_6.value,
                    ]
                )
            )

            generated_report = report_generator.generate_report()
            json_data = generated_report.parse_to_json()

            print(f'--------generated_report : {content['start']} ~ {content['end']}-------- [elapsed time : {time() - start_time:.2f} sec]')
            for key, value in json_data.items():
                print(key, ':', value)