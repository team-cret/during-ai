import importlib
import logging

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

class MotionAnalyzerV0(MotionAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
        self.set_logger()
    
    def set_logger(self) -> None:
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_analyzer(self) -> None:
        self.analyzer_type = ServiceConfig.MOTION_ANALYZER_V0_TYPE.value
        self.module_name = ServiceConfig.MOTION_ANALYZER_V0_MODULE.value
        self.class_name = ServiceConfig.MOTION_ANALYZER_V0_CLASS.value

        module = importlib.import_module(f'ai_model.{self.analyzer_type}.{self.module_name}')
        ai_model_class = getattr(module, self.class_name)

        self.ai_model = ai_model_class()

        if self.analyzer_type == 'embedding':
            self.get_embedded_motions()
    
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
            if self.analyzer_type == 'classification':
                return self.analyze_by_classification(chat.message)
            elif self.analyzer_type == 'embedding':
                return self.analyze_by_embedding(chat.message)
            elif self.analyzer_type == 'generation':
                return self.analyze_by_llm(chat)
            
            # 알 수 없는 analyzer_type인 경우
            return self.return_none_motion()
        except Exception as e:
            # 예외 발생 시 로깅 추가
            print(f"Motion analysis error: {str(e)}")
            # 오류 발생 시 기본값 반환
            return self.return_none_motion()

    def analyze_by_classification(self, message:str) -> Motion:
        self.ai_model: TextClassification
        classify_result = self.ai_model.classify_text(message)

        if classify_result['scores'][0] < 0.5:
            return self.return_none_motion()
        
        if np.var(classify_result['scores']) < 0.03:
            return self.return_none_motion()

        return Motion(
            motion=classify_result['motions'][0],
            motion_id=motion_to_id[classify_result['motions'][0]],
        )

    def analyze_by_embedding(self, message:str) -> Motion:
        self.ai_model: Embedding
        embedded_chat = self.ai_model.embed_text(message)

        max_similarity = 0
        max_motion_id = -1
        for motion_id, embedded_motion in self.embedded_motions.items():
            similarity = self.similarity(embedded_chat, embedded_motion)

            if similarity > 0.5 and max_similarity < similarity:
                max_similarity = similarity
                max_motion_id = motion_id
        
        if max_motion_id == -1:
            return self.return_none_motion()
        
        return Motion(
            motion=motions[max_motion_id]['motion'],
            motion_id=max_motion_id
        )

    def similarity(self, v1, v2) -> float:
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def get_embedded_motions(self) -> list:
        embedded_data = np.load(f'data/embedded_data/{self.module_name}.npz')

        self.embedded_motions = {}
        for key, value in embedded_data.items():
            self.embedded_motions[int(key)] = value
    
    def analyze_by_llm(self, chat:CoupleChat) -> Motion:
        self.ai_model: Generation
        response = self.ai_model.analyze_motion(chat=chat)

        return response