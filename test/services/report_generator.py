from service.report.report_generator import ReportGenerator

from datetime import datetime

class ReportGeneratorTester:
    def __init__(self):
        self.setup_for_test()
        self.setup_test_contents()

    def setup_for_test(self):
        self.report_generator = ReportGenerator()
        self.couple_id = 'test'

    def setup_test_contents(self):
        self.test_contents = [
            {'start' : datetime(2022, 1, 1), 'end' : datetime(2022, 2, 1)},
        ]

    def test(self):
        for content in self.test_contents:
            generated_report = self.report_generator.generate_report(self.couple_id, content['start'], content['end'])
            json_data = generated_report.parse_to_json()

            print(f'--------generated_report : {content['start']} ~ {content['end']}--------')
            for key, value in json_data.items():
                print(key, ':', value)