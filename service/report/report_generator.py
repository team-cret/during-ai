from database.db import DB
from model.data_model import ReportRequest, CoupleChat, Report
from service.report.statistical_analyzer import StatisticalAnalyzer
from service.report.contents_generator import ContentsGenerator
from service.report.ai_analyzer import AIAnalyzer
from setting.service_config import ServiceConfig

class ReportGenerator:
    def __init__(self, report_request:ReportRequest):
        self.set_report_generator(report_request)

    def set_report_generator(self, report_request:ReportRequest):
        self.report_request = report_request
        self.statistical_analyzer = StatisticalAnalyzer()
        self.contents_generator = ContentsGenerator()
        self.ai_analyzer = AIAnalyzer()
        self.db = DB()
    
    def generate_report(self) -> Report:
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
    
    def load_couple_chat(self) -> list[CoupleChat]:
        return self.db.get_couple_chat_for_period(self.report_request)

    def decide_report_type(self) -> str:
        if len(self.couple_chat) < 500:
            return ServiceConfig.REPORT_TYPE_1.value
        elif len(self.couple_chat) >= 500:
            return ServiceConfig.REPORT_TYPE_2.value
    
    def generate_small_report(self):
        pass

    def generate_big_report(self) -> None:
        self.analyze_statistics()
        self.analyze_by_ai()
    
    def analyze_statistics(self) -> None:
        statistical_report:Report = self.statistical_analyzer.analyze_statistics(self.couple_chat, self.report_request)

        self.report.response_time_zone = statistical_report.response_time_zone
        self.report.concurrent_time_zone = statistical_report.concurrent_time_zone
        self.report.frequently_used_emotion = statistical_report.frequently_used_emotion
        self.report.number_of_love_words = statistical_report.number_of_love_words
        self.report.average_reply_term = statistical_report.average_reply_term

    def analyze_by_ai(self) -> None:
        ai_report:Report = self.ai_analyzer.analyze_by_ai(self.couple_chat)

        self.report.MBTI = ai_report.MBTI
        self.report.frequently_talked_topic = ai_report.frequently_talked_topic
        self.report.frequency_of_affection = ai_report.frequency_of_affection
        self.report.sweetness_score = ai_report.sweetness_score
