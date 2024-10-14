import logging
from collections import Counter
from tqdm import tqdm

from ai_model.classification.pogjin_roberta import PongjinRobertaTextClassification
from model.data_model import Report, CoupleChat
from setting.logger_setting import logger_setting
    
class AIAnalyzer:
    def __init__(self):
        self.ai_report:Report = Report()
        logger_setting()
        self.logger = logging.getLogger(__name__)

    def analyze_by_ai(self, couple_chat:list[CoupleChat]):
        try: 
            self.couple_chat = couple_chat
            self.analyze_mbti()
            self.analyze_frequently_talked_topic()
            self.analyze_frequency_of_affection()
            self.analyze_sweetness_score()
        except Exception as e:
            self.logger.error(f"Error in analyzing by AI: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing by AI")

        return self.ai_report

    def analyze_mbti(self):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error in analyzing MBTI: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing MBTI")
        
    def analyze_frequently_talked_topic(self):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error in analyzing frequently talked topic: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing frequently talked topic")

    def analyze_frequency_of_affection(self):
        try:
            ai_classifier = PongjinRobertaTextClassification()

            tf_affection = ai_classifier.is_affection_batch_classification(
                [chat.message for chat in self.couple_chat[:500]]
            )

            time_period = self.couple_chat[-1].timestamp - self.couple_chat[0].timestamp
            self.ai_report.frequency_of_affection = time_period / (Counter(tf_affection)[True] * len(self.couple_chat) / 500)
        except Exception as e:
            self.logger.error(f"Error in analyzing frequency of affection: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing frequency of affection")
        
    def analyze_sweetness_score(self):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error in analyzing sweetness score: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing sweetness score")