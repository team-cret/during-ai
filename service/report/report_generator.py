from model.report import Report
from model.data_model import CoupleChat
from service.report.statistical_analyzer import StatisticalAnalyzer
from datetime import datetime
from database.db import DB

class ReportGenerator:
    def __init__(self):
        self.statistical_analyzer = StatisticalAnalyzer()
        self.db = DB()

    def generate_report(self, couple_id:str, start_date:datetime, end_date:datetime) -> Report:
        couple_chat = self.load_couple_chat(couple_id, start_date, end_date)
        report_type = self.decide_report_type(couple_chat)

        report = Report()
        if report_type == 'small':
            report = self.load_connection_log()
        else:
            report = self.analyze_statistics(report, couple_chat)
        return report
    
    def load_couple_chat(self, couple_id:str, start_date:datetime, end_date:datetime) -> list[CoupleChat]:
        return self.db.load_chat_data_for_period(couple_id, start_date, end_date)
    
    def generate_image(self) -> Report:
        return Report(
            image='image_path'
        )

    def load_connection_log(self):
        log = []
        return log

    
    def decide_report_type(self, couple_chat:list[CoupleChat]) -> str:
        if len(couple_chat) < 150:
            return 'small'
        else:
            return 'big'

    def analyze_statistics(self, report:Report, couple_chat) -> Report:
        self.statistical_analyzer.analyze_statistics(couple_chat)

        report.average_reply_term = self.statistical_analyzer.statistical_report.average_reply_term
        report.concurrent_time_zone = self.statistical_analyzer.statistical_report.concurrent_time_zone
        report.frequently_used_emotion = self.statistical_analyzer.statistical_report.frequently_used_emotion
        report.response_time_zone = self.statistical_analyzer.statistical_report.response_time_zone
        return report
