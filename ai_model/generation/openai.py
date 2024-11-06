import os
import logging

from openai import OpenAI

from data.gomdu_prompt import GomduPrompt
from data.motion_analysis_prompt import motion_analysis_prompt
from data.ai_report_prompt import ai_report_prompt, ai_main_event_prompt
from model.data_model import CoupleChat, Motion, RetrievedData, MotionJson, AIReportAnalyzeResponse, AIReportMainEventResponse
from setting.config import Config
from setting.model_config import ModelConfig
from setting.service_config import ServiceConfig
from setting.logger_setting import logger_setting

class OpenAITextGenerator:
    def __init__(self) -> None:
        self.set_model()
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_model(self) -> None:
        self.client = OpenAI(api_key=os.environ[Config.OPENAI_API_KEY.value])
        
    def generate_text_chat_mode(self, user_id:str, user_prompt:str, retrieved_prompt:list[RetrievedData], history:list[dict], is_stream:bool = False) -> str:
        try:
            gomdu_prompt = GomduPrompt()
            gomdu_prompt.set_user_id(user_id[:ServiceConfig.GOMDU_CHAT_USER_ID_LENGTH.value])

            processed_history = [
                {
                    'role' : 'system',
                    'content' : gomdu_prompt.gomdu_system_prompt
                }
            ]
        
            for story in history:
                if story['role'] == ServiceConfig.GOMDU_CHAT_AI_NAME.value:
                    processed_history.append({
                        'role' : 'assistant',
                        'content' : story['text']
                    })
                elif story['role'] == ServiceConfig.GOMDU_CHAT_USER_NAME.value:
                    processed_history.append({
                        'role' : 'user',
                        'content' : story['text']
                    })
                elif story['role'] == ServiceConfig.GOMDU_CHAT_SYSTEM_NAME.value:
                    processed_history.append({
                        'role' : 'system',
                        'content' : story['content']
                    })
            
            processed_history.append({
                'role' : 'user',
                'content' : user_prompt
            })
            processed_history.append({
                'role' : 'system',
                'content' : f'당신이 참고 할 수 있는 커플의 대화데이터는 다음과 같습니다. <<<{retrieved_prompt}>>> 이 부분을 참고해서 대답하세요. 이 부분을 참고해도 모르겠으면 모른다고 대답하세요.'
            })

            response = self.client.chat.completions.create(
                model=ModelConfig.OPENAI_LLM_MODEL.value,
                messages=processed_history,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error in llm model generating text chat mode (openai): {str(e)}", exc_info=True)
            raise Exception("Error in llm model generating text chat mode")

    def analyze_motion(self, chat:CoupleChat) -> Motion:
        result = self.client.beta.chat.completions.parse(
            model='gpt-4o-mini-2024-07-18',
            messages=[
                {'role' : 'system', 'content' : motion_analysis_prompt},
                {'role' : 'user', 'content' : chat.message}
            ],
            response_format=MotionJson,
        )
        return result.choices[0].message.parsed
    
    def analyze_chat_data(self, chat_document:str) -> str:
        result = self.client.beta.chat.completions.parse(
            model='gpt-4o-mini',
            messages=[
                {'role' : 'system', 'content' : ai_report_prompt},
                {'role' : 'user', 'content' : chat_document}
            ],
            response_format=AIReportAnalyzeResponse
        )
        return result.choices[0].message.parsed
    
    def analyze_main_event_from_chat(self, chat_document:str) -> str:
        result = self.client.beta.chat.completions.parse(
            model='gpt-4o-mini',
            messages=[
                {'role' : 'system', 'content' : ai_main_event_prompt},
                {'role' : 'user', 'content' : chat_document}
            ],
            response_format=AIReportMainEventResponse
        )
        return result.choices[0].message.parsed