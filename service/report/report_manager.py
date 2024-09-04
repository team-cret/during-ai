from database.db import DB
from model.data_model import Report, ReportRequest
from service.report.report_generator import ReportGenerator

class ReportManager:
    def __init__(self):
        self.generators = {}
        
    def make_new_generator(self, report_request:ReportRequest):
        self.generators[report_request.couple_id] = ReportGenerator(report_request)

    def generate_report(self, report_request:ReportRequest) -> Report:
        self.make_new_generator(report_request)
        return self.generators[report_request.couple_id].generate_report()
