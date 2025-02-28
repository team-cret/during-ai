import importlib
import logging
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from ai_model.embedding.embedding import Embedding
from ai_model.classification.text_classification import TextClassification
from ai_model.generation.generation import Generation
from data.motions import motion_to_id, motions
from model.data_model import CoupleChat, Motion
from setting.service_config import ServiceConfig
from setting.logger_setting import logger_setting
from service.motion_analysis.keyword_analyzer import KeywordAnalyzer
from service.motion_analysis.motion_analyzer import MotionAnalyzer

class MotionAnalyzerV01(MotionAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
        self.set_logger()
        self.set_motion_distribution()
    
    def set_motion_distribution(self) -> None:
        self.sentiment_motions = [value['motion'] for key, value in motions.items() if 1000 <= key < 2000]
        self.action_motions = [value['motion'] for key, value in motions.items() if 2000 <= key < 4000]
        # self.object_motions = [value['motion'] for key, value in motions.items() if 3000 <= key < 4000]
        self.label_classification = ['감정 표현', '행동']

        self.sentiment_hypothesis = '이 문장에서 느껴지는 감정은 {}이다.'
        self.action_hypothesis = '이 문장을 통해 화자가 할 것 같은 행동은 {}이다.'
        self.label_hypothesis = '이 문장을 말하면서 {}을 하는 것이 자연스럽다'

        self.labels = [
            self.sentiment_motions,
            self.action_motions,
            # self.object_motions,
            self.label_classification
        ]

        self.hypotheses = [
            self.sentiment_hypothesis,
            self.action_hypothesis,
            # self.object_hypothesis,
            self.label_hypothesis
        ]

    def set_logger(self) -> None:
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_analyzer(self) -> None:
        self.analyzer_type = ServiceConfig.MOTION_ANALYZER_V0_1_TYPE.value
        self.module_name = ServiceConfig.MOTION_ANALYZER_V0_1_MODULE.value
        self.class_name = ServiceConfig.MOTION_ANALYZER_V0_1_CLASS.value

        module = importlib.import_module(f'ai_model.{self.analyzer_type}.{self.module_name}')
        ai_model_class = getattr(module, self.class_name)

        self.ai_model = ai_model_class()
    
    def return_none_motion(self) -> Motion:
        return Motion(
            motion='없음',
            motion_id=9999
        )

    def analyze_motion(self, chat: CoupleChat) -> Motion:
        try:
            # keyword analyze
            if keyword := self.keyword_analyzer.is_keyword(chat.message):
                return keyword
            
            # length limit
            if len(chat.message) > 30:
                return self.return_none_motion()
            
            # ai model analyze
            return self.analyze_by_classification(chat.message)
        except Exception as e:
            self.logger.info(f'motion analyzerv01 error: {str(e)}')
            return self.return_none_motion()

    def analyze_by_classification(self, message: str) -> Motion:
        try:
            self.ai_model: TextClassification

            with ThreadPoolExecutor() as executor:
                parallel_result = list(
                    executor.map(
                        self.ai_model.classify_text_by_hypothesis, 
                        [message] * len(self.labels),
                        self.hypotheses,
                        self.labels
                    )
                )

                if parallel_result[-1]['labels'][0] == '감정 표현':
                    return self.return_best_value(parallel_result[0])
                elif parallel_result[-1]['labels'][0] == '행동':
                    return self.return_best_value(parallel_result[1])
                return self.return_none_motion()
        except Exception as e:
            self.logger.error(f"classification error: {str(e)}")
            return self.return_none_motion()
    
    def return_best_value(self, result: list[dict]) -> str:
        if result['scores'][0] < 0.5:
            return self.return_none_motion()
        
        if np.var(result['scores']) < 0.03:
            return self.return_none_motion()
        
        return Motion(
            motion=result['labels'][0],
            motion_id=motion_to_id[result['labels'][0]],
        )

# test type
# 0 : general
# 1 : mixed
# 2 : cuty tone
# 3 : space, punctuation
# 4 : honorfics
# 5 : difficult