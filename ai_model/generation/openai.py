import os

from openai import OpenAI

from data.gomdu_prompt import gomdu_system_prompt
from data.motion_analysis_prompt import motion_analysis_prompt
from model.data_model import CoupleChat, Motion, RetrievedData, MotionJson
from setting.config import Config
from setting.model_config import ModelConfig
from setting.service_config import ServiceConfig

class OpenAITextGenerator:
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        self.client = OpenAI(api_key=os.environ[Config.OPENAI_API_KEY.value])
        
    def generate_text_chat_mode(self, user_prompt:str, retrieved_prompt:list[RetrievedData], history:list[dict], is_stream:bool = False) -> str:
        processed_history = [
            {
                'role' : 'system',
                'content' : gomdu_system_prompt
            },
            {
                'role' : 'system',
                'content' : f'이번에 답할 때는 커플 대화내용 중에서 [{retrieved_prompt}] 이 부분을 참고해서 대답해줘 이 부분을 참고해도 모르겠으면 모른다고 대답해줘'
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

        response = self.client.chat.completions.create(
            model=ModelConfig.OPENAI_LLM_MODEL.value,
            messages=processed_history,
        )
        
        return response.choices[0].message.content

    def analyze_motion(self, chat:CoupleChat) -> Motion:
        result = self.client.beta.chat.completions.parse(
            model='gpt-4o-mini-2024-07-18',
            messages=[
                {'role' : 'system', 'content' : motion_analysis_prompt},
                {'role' : 'user', 'content' : chat.message}
            ],
            response_format=MotionJson,
        )
        return Motion(
            motion = result.choices[0].message.parsed.motion,
            motion_id = result.choices[0].message.parsed.motion_id
        )