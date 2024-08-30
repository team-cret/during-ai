import importlib

from service.gomdu.gomdu import Gomdu
from service.report.report_generator import ReportGenerator
from service.motion_analysis.motion_analyzer import MotionAnalyzer
from setting.service_config import ServiceConfig
from setting.init_setting import init_setting


class ServerManager:
    def __init__(self):
        init_setting()
        self.service_setting()
    
    def service_setting(self):
        module = importlib.import_module(f'service.sentiment_analysis.{ServiceConfig.CURRENT_SENTIMENT_ANALYZER_MODULE.value}')
        analyzer_class = getattr(module, ServiceConfig.CURRENT_SENTIMENT_ANALYZER_CLASS.value)
        self.motion_analyzer:MotionAnalyzer = analyzer_class()

        self.gomdu = Gomdu()
        self.report_generator = ReportGenerator()