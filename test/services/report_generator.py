from service.report.report_generator import ReportGenerator
from datetime import datetime

class ReportGeneratorTester:
    def __init__(self):
        couple_id = 'test'
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 2, 1)
        self.report_generator = ReportGenerator(couple_id, start_date, end_date)

    def test(self):
        self.report_generator.generate_report()
        json = self.report_generator.report.parse_to_json()
        for key, value in json.items():
            print(key, ':', value)