from service.report.report_generator import ReportGenerator
from datetime import datetime

class ReportGeneratorTester:
    def __init__(self):
        self.report_generator = ReportGenerator()

    def test(self):
        couple_id = 'test'
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 2, 1)

        generated_report = self.report_generator.generate_report(couple_id, start_date, end_date)
        json = generated_report.parse_to_json()

        for key, value in json.items():
            print(key, ':', value)