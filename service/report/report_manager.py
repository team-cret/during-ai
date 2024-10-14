from cachetools import TTLCache
from database.db import DB
from model.data_model import Report, ReportRequest
from service.report.report_generator import ReportGenerator

class ReportManager:
    def __init__(self):
        self.generators = {}
        
    def make_new_generator(self, report_request:ReportRequest):
        self.generators[report_request.couple_id] = TTLCache(maxsize=2, ttl=3600)
        self.generators[report_request.couple_id]['generator'] = ReportGenerator(report_request)

    def generate_report(self, report_request:ReportRequest) -> Report:
        if report_request.couple_id not in self.generators:
            self.make_new_generator(report_request)

        return self.generators[report_request.couple_id]['generator'].generate_report()