from service.gomdu.chat_generator import ChatGenerator
from service.report.report_generator import ReportGenerator
from service.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer

from setting.service_config import ServiceConfig

import importlib

class ServerManager:
    def __init__(self):
        self.init_setting()
        self.service_setting()
    
    def service_setting(self):
        module = importlib.import_module(f'service.sentiment_analysis.{ServiceConfig.CURRENT_SENTIMENT_ANALYZER.value}')
        analyzer_class = getattr(module, ServiceConfig.CURRENT_SENTIMENT_ANALYZER_CLASS.value)
        self.sentiment_analyzer:SentimentAnalyzer = analyzer_class()

        self.gomdu = ChatGenerator()
        self.report_generator = ReportGenerator()