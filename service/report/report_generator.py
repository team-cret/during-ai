import logging

from database.db import DB
from model.data_model import ReportRequest, CoupleChat, Report
from service.report.statistical_analyzer import StatisticalAnalyzer
from service.report.contents_generator import ContentsGenerator
from service.report.ai_analyzer import AIAnalyzer
from setting.service_config import ServiceConfig
from setting.logger_setting import logger_setting

class ReportGenerator:
    def __init__(self, report_request:ReportRequest):
        self.set_report_generator(report_request)
        logger_setting()
        self.logger = logging.getLogger(__name__)

    def set_report_generator(self, report_request:ReportRequest):
        self.report_request = report_request
        self.statistical_analyzer = StatisticalAnalyzer()
        self.contents_generator = ContentsGenerator()
        self.ai_analyzer = AIAnalyzer()
        self.db = DB()
        self.is_making = False
    
    def generate_report(self) -> Report:
        try:
            # load couple chat
            self.couple_chat = self.load_couple_chat()

            # decide report type
            report_type = self.decide_report_type()

            # generate report object
            self.report = Report()
            self.report.report_type = report_type

            if report_type == ServiceConfig.REPORT_TYPE_1.value:
                self.generate_small_report()
            elif report_type == ServiceConfig.REPORT_TYPE_2.value:
                self.generate_big_report()
            return self.report
        except Exception as e:
            self.logger.error(f"Error in generating report: {str(e)}", exc_info=True)
            raise Exception("Error in generating report")
    
    def load_couple_chat(self) -> list[CoupleChat]:
        try:
            return self.db.get_couple_chat_for_period(self.report_request)
        except Exception as e:
            self.logger.error(f"Error in loading couple chat: {str(e)}", exc_info=True)
            raise Exception("Error in loading couple chat")

    def decide_report_type(self) -> str:
        try:
            if len(self.couple_chat) < 500:
                return ServiceConfig.REPORT_TYPE_1.value
            elif len(self.couple_chat) >= 500:
                return ServiceConfig.REPORT_TYPE_2.value
        except Exception as e:
            self.logger.error(f"Error in deciding report type: {str(e)}", exc_info=True)
            raise Exception("Error in deciding report type")

    def generate_small_report(self):
        pass

    def generate_big_report(self) -> None:
        try:
            self.analyze_statistics()
            self.analyze_by_ai()
        except Exception as e:
            self.logger.error(f"Error in generating big report: {str(e)}", exc_info=True)
            raise Exception("Error in generating big report")
    
    def analyze_statistics(self) -> None:
        try:
            statistical_report:Report = self.statistical_analyzer.analyze_statistics(self.couple_chat, self.report_request)

            self.report.response_time_zone = statistical_report.response_time_zone
            self.report.concurrent_time_zone = statistical_report.concurrent_time_zone
            self.report.frequently_used_emotion = statistical_report.frequently_used_emotion
            self.report.number_of_love_words = statistical_report.number_of_love_words
            self.report.average_reply_term = statistical_report.average_reply_term
        except Exception as e:
            self.logger.error(f"Error in analyzing statistics: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing statistics")

    def analyze_by_ai(self) -> None:
        try:
            ai_report:Report = self.ai_analyzer.analyze_by_ai(self.couple_chat)

            self.report.MBTI = ai_report.MBTI
            self.report.frequently_talked_topic = ai_report.frequently_talked_topic
            self.report.frequency_of_affection = ai_report.frequency_of_affection
            self.report.sweetness_score = ai_report.sweetness_score
        except Exception as e:
            self.logger.error(f"Error in analyzing by ai: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing by ai")