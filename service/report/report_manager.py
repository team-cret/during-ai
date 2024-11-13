import logging
from cachetools import TTLCache

from model.data_model import Report, ReportRequest
from service.report.report_generator import ReportGenerator
from setting.logger_setting import logger_setting

class ReportManager:
    def __init__(self):
        self.generators = {}
        logger_setting()
        self.logger = logging.getLogger(__name__)
        
    def make_new_generator(self, report_request:ReportRequest):
        try:
            self.generators[report_request.couple_id] = TTLCache(maxsize=2, ttl=7200)
            self.generators[report_request.couple_id]['generator'] = ReportGenerator(report_request)
            self.logger.info(f"Success to make new generator for couple_id: {report_request.couple_id}")
        except Exception as e:
            self.logger.error(f"Error in making new generator: {str(e)}", exc_info=True)
            raise Exception("Error in making new generator")

    def generate_report(self, report_request:ReportRequest) -> Report:
        try:
            if report_request.couple_id not in self.generators:
                self.make_new_generator(report_request)

            if self.generators[report_request.couple_id]['generator'].is_making:
                raise Exception("Report is already being generated")
            return self.generators[report_request.couple_id]['generator'].generate_report()
        except Exception as e:
            self.logger.error(f"Error in generating report: {str(e)}", exc_info=True)
            raise Exception("Error in generating report")