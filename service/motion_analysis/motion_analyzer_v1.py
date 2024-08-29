import importlib

import numpy as np

from ai_model.embedding.embedding import Embedding
from data.motions import motion_to_id, motions
from model.data_model import CoupleChat, Motion
from setting.service_config import ServiceConfig
from service.motion_analysis.keyword_analyzer import KeywordAnalyzer
from service.motion_analysis.motion_analyzer import MotionAnalyzer

class MotionAnalyzerV1(MotionAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
    
    def set_analyzer(self) -> None:
        self.module_names = [
            ServiceConfig.MOTION_ANALYZER_V1_MODULE1.value,
            ServiceConfig.MOTION_ANALYZER_V1_MODULE2.value,
            ServiceConfig.MOTION_ANALYZER_V1_MODULE3.value,
        ]

        self.class_names = [
            ServiceConfig.MOTION_ANALYZER_V1_CLASS1.value,
            ServiceConfig.MOTION_ANALYZER_V1_CLASS2.value,
            ServiceConfig.MOTION_ANALYZER_V1_CLASS3.value,
        ]

        modules = [
            importlib.import_module(f'ai_model.classification.{module_name}')
            for module_name in self.module_names
        ]

        ai_model_classes = [
            getattr(module, class_name)
            for module, class_name in zip(modules, self.class_names)
        ]
        
        self.ai_models = [
            ai_model_class()
            for ai_model_class in ai_model_classes
        ]

    def analyze_motion(self, chat:CoupleChat) -> Motion:
        if self.keyword_analyzer.is_keyword(chat.message):
            return self.keyword_analyzer.is_keyword(chat.message)
        
        classify_results = [ai_model.classify_text(chat.message) for ai_model in self.ai_models]
        
        integrated_result = {}
        for classify_result in classify_results:
            for motion, score in zip(classify_result['motions'], classify_result['scores']):
                if motion in integrated_result:
                    integrated_result[motion] += score ** 2
                else:
                    integrated_result[motion] = score ** 2
        
        classify_result = {
            'motions' : [motion for motion, _ in sorted(integrated_result.items(), key=lambda x:x[1], reverse=True)],
            'scores' : [score for _, score in sorted(integrated_result.items(), key=lambda x:x[1], reverse=True)],
        }
        return {
            'motion': classify_result['motions'][0], 
            'motion_id': motion_to_id[classify_result['motions'][0]],
        }