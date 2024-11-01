import logging
from collections import Counter
from tqdm import tqdm

import uuid

from ai_model.tokenizer.tiktoken_tokenizer import TiktokenTokenizer
from ai_model.generation.openai import OpenAITextGenerator
from ai_model.classification.pogjin_roberta import PongjinRobertaTextClassification
from model.data_model import Report, CoupleChat, AIReportAnalyzeResponse, AIReportMainEventResponse
from setting.logger_setting import logger_setting
    
class AIAnalyzer:
    def __init__(self):
        self.ai_report:Report = Report()
        self.tokenizer = TiktokenTokenizer()
        logger_setting()
        self.logger = logging.getLogger(__name__)

    def analyze_by_ai(self, couple_chat:list[CoupleChat], couple_member_ids:list[str]) -> Report:
        try: 
            self.couple_chat = couple_chat
            self.couple_member_ids = couple_member_ids
            self.analyze_by_llm_json()
            self.logger.info("Success to Analyzed by LLM JSON")
            self.analyze_frequency_of_affection()
            self.logger.info("Success to Analyzed frequency of affection by NLI")
            return self.ai_report
        except Exception as e:
            self.logger.error(f"Error in analyzing by AI: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing by AI")
    
    def retrieve_main_event(self, couple_chat:list[CoupleChat]) -> str:
        try:
            ai_model = OpenAITextGenerator()
            merged_chat = ' '.join([
                f'[{chat.user_id[:4]}] : {chat.message}'
                for chat in couple_chat
            ])
            ai_main_event_response = ai_model.analyze_main_event_from_chat(merged_chat)
            ai_main_event_response:AIReportMainEventResponse
            return ai_main_event_response.main_event
        except Exception as e:
            self.logger.error(f"Error in retrieving main event: {str(e)}", exc_info=True)
            raise Exception("Error in retrieving main event")

    def analyze_by_llm_json(self):
        try:
            ai_model = OpenAITextGenerator()
            merged_chat = ' '.join([
                f'[{chat.user_id[:4]}] : {chat.message}'
                for chat in self.couple_chat
            ])
            total_token_length = self.tokenizer.calculate_token_length(merged_chat)
            max_token = 100_000
            if total_token_length > max_token:
                merged_chat = merged_chat[int(len(merged_chat)*(1-max_token/total_token_length)):]
            iteration = 0
            while iteration < 3:
                ai_analyze_response = ai_model.analyze_chat_data(merged_chat)
                ai_analyze_response:AIReportAnalyzeResponse
                mbti = ai_analyze_response.MBTI
                mbti = mbti.split(', ')
                result_mbti = []
                for mbt in mbti:
                    mb = mbt.split(':')
                    for user_id in self.couple_member_ids:
                        if mb[0] == user_id[:4]:
                            result_mbti.append((user_id, mb[1]))
                            break
                self.ai_report.MBTI = result_mbti
                self.ai_report.sweetness_score = ai_analyze_response.sweetness_score
                self.ai_report.frequently_talked_topic = list(ai_analyze_response.frequently_talked_topic.split(', '))
                if self.check_parse_correction():
                    break
                iteration += 1
        except Exception as e:
            self.logger.error(f"Error in analyzing by LLM JSON: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing by LLM JSON")
    
    def check_parse_correction(self) -> bool:
        try:
            if len(self.ai_report.MBTI) != 2:
                return False
            uuid.UUID(self.ai_report.MBTI[0][0], 4)
            uuid.UUID(self.ai_report.MBTI[1][0], 4)
            if int(self.ai_report.sweetness_score) < 0 or int(self.ai_report.sweetness_score) > 100:
                return False
            return True
        except Exception as e:
            self.logger.error(f"Error in checking parse correction: {str(e)}", exc_info=True)
            return False

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
            self.ai_report.frequency_of_affection = time_period / ((Counter(tf_affection)[True]+1) * len(self.couple_chat) / 500)
        except Exception as e:
            self.logger.error(f"Error in analyzing frequency of affection: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing frequency of affection")
        
    def analyze_sweetness_score(self):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Error in analyzing sweetness score: {str(e)}", exc_info=True)
            raise Exception("Error in analyzing sweetness score")
