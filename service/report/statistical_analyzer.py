from model.data_model import CoupleChat
from setting.service_config import ServiceConfig
from model.data_model import Report

class StatisticalAnalyzer:
    def __init__(self):
        self.statistical_report:Report = Report()

    def analyze_statistics(self, couple_chat:list[CoupleChat]):
        self.couple_chat = couple_chat
        self.analyze_response_time_zone()
        self.analyze_concurrent_time_zone()
        self.analyze_frequently_used_emotion()
        self.analyze_average_reply_term()

    def analyze_response_time_zone(self):
        response_time_zone = [0 for _ in range(round(1440/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
        for chat in self.couple_chat:
            response_time_zone[(chat.timestamp.hour * 60 + chat.timestamp.minute) // ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value] += 1
        self.statistical_report.response_time_zone = response_time_zone

    def analyze_concurrent_time_zone(self):
        concurrent_time_zone = [0 for _ in range(round(24/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
        pass

    def analyze_frequently_used_emotion(self):
        emotions = {}
        for chat in self.couple_chat:
            if chat.chat_type == 'emotion':
                if emotions[chat.message] == None:
                    emotions[chat.message] = 1
                else:
                    emotions[chat.message] += 1
        self.statistical_report.frequently_used_emotion = sorted(
            list(emotions.items()),
            key=lambda x: -x[1],
        )[:6]

    
    def analyze_average_reply_term(self):
        time_period = self.couple_chat[-1].timestamp - self.couple_chat[0].timestamp
        
        for i in range(1, len(self.couple_chat)):
            previous_chat = self.couple_chat[i-1]
            current_chat = self.couple_chat[i]
        
        self.statistical_report.average_reply_term = time_period / len(self.couple_chat)