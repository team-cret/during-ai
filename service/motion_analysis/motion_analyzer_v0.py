import importlib

import numpy as np

from ai_model.embedding.embedding import Embedding
from ai_model.classification.text_classification import TextClassification
from ai_model.generation.generation import Generation
from data.motions import motion_to_id, motions
from model.data_model import CoupleChat, Motion
from setting.service_config import ServiceConfig
from service.motion_analysis.keyword_analyzer import KeywordAnalyzer
from service.motion_analysis.motion_analyzer import MotionAnalyzer


class MotionAnalyzerV0(MotionAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
    
    def set_analyzer(self) -> None:
        self.analyzer_type = ServiceConfig.MOTION_ANALYZER_V0_TYPE.value
        self.module_name = ServiceConfig.MOTION_ANALYZER_V0_MODULE.value
        self.class_name = ServiceConfig.MOTION_ANALYZER_V0_CLASS.value
        self.ai_model_name = ServiceConfig.MOTION_ANALYZER_V0_AI_MODEL_NAME.value

        module = importlib.import_module(f'ai_model.{self.analyzer_type}.{self.module_name}')
        ai_model_class = getattr(module, self.class_name)

        self.ai_model = ai_model_class()

        if self.analyzer_type == 'embedding':
            self.get_embedded_motions()

    def analyze_motion(self, chat:CoupleChat) -> Motion:
        if keyword := self.keyword_analyzer.is_keyword(chat.message):
            return Motion(
                motion=keyword,
                motion_id=motion_to_id[keyword]
            )
        
        if self.analyzer_type == 'classification':
            return self.analyze_by_classification(chat.message)
        elif self.analyzer_type == 'embedding':
            return self.analyze_by_embedding(chat.message)
        elif self.analyzer_type == 'llm_json':
            return self.analyze_by_llm_json(chat.message)
    
    def analyze_by_classification(self, message:str) -> Motion:
        self.ai_model: TextClassification
        classify_result = self.ai_model.classify_text(message)

        return {
            'motion': classify_result['motions'][0], 
            'motion_id': motion_to_id[classify_result['motions'][0]],
        }

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
            return Motion(
                motion='없음',
                motion_id=-1
            )
        
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

        print(response)
        return Motion(
            motion='없음',
            motion_id=-1
        )