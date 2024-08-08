from model.report import Report
from service.report.statistical_analyzer import StatisticalAnalyzer
from datetime import datetime
from database.db import DB

class ReportGenerator:
    def __init__(self, couple_id:str, start_date:datetime, end_date:datetime):
        self.couple_id = couple_id
        self.start_date = start_date
        self.end_date = end_date
        self.report:Report = Report()
        self.statistical_analyzer = StatisticalAnalyzer()
        self.db = DB()

    def generate_report(self, ):
        self.couple_chat = self.load_couple_chat()
        self.decide_report_type()
        if self.report.report_type == 'small':
            self.load_connection_log()
        else:
            self.analyze_statistics()
    
    def load_couple_chat(self):
        return self.db.load_chat_data_for_period(
            self.couple_id,
            self.start_date,
            self.end_date
        )
    
    def generate_image(self):
        return 'image'

    def load_connection_log(self):
        log = []
        return log

    
    def decide_report_type(self):
        if len(self.couple_chat) < 150:
            self.report.report_type = 'small'
        else:
            self.report.report_type = 'big'

    def analyze_statistics(self):
        self.statistical_analyzer.analyze_statistics(self.couple_chat)
        self.report.average_reply_term = self.statistical_analyzer.statistical_report.average_reply_term
        self.report.concurrent_time_zone = self.statistical_analyzer.statistical_report.concurrent_time_zone
        self.report.frequently_used_emotion = self.statistical_analyzer.statistical_report.frequently_used_emotion
        self.report.response_time_zone = self.statistical_analyzer.statistical_report.response_time_zone
