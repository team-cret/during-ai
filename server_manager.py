import sys
import os
import importlib
from setting.config import Config
from setting.service_config import ServiceConfig
from service.gomdu.chat_generator import ChatGenerator
from service.report.report_generator import ReportGenerator
from service.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer

class ServerManager:
    def __init__(self):
        self.init_setting()
        self.service_setting()

    def init_setting(self):
        dir_path = os.path.abspath(os.path.dirname('during-ai'))
        sys.path.insert(0, dir_path)
        print('dir_path : ', dir_path)

        from setting.api_key_setting import APIKeySetting
        api_key_setter = APIKeySetting()
        api_key_setter.set_api_key()
    
    def service_setting(self):
        module = importlib.import_module(f'service.sentiment_analysis.{ServiceConfig.CURRENT_SENTIMENT_ANALYZER.value}')
        analyzer_class = getattr(module, ServiceConfig.CURRENT_SENTIMENT_ANALYZER_CLASS.value)
        self.sentiment_analyzer:SentimentAnalyzer = analyzer_class()

        self.gomdu = ChatGenerator()
        self.report_generator = ReportGenerator()