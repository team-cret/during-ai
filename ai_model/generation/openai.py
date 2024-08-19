import os
from setting.config import Config
from data.gomdu_prompt import gomdu_system_prompt
from openai import OpenAI

class OpenAITextGenerator:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=os.environ[Config.OPENAI_API_KEY.value])
        
    def generate_text_by_chat_bot(self, user_prompt:str, history:list[dict], is_stream:bool = False) -> str:
        processed_history = [
            {
                'role' : 'system',
                'content' : gomdu_system_prompt
            }
        ]

        for story in history:
            if story['role'] == 'assi':
                processed_history.append({
                    'role' : 'assistant',
                    'content' : story['text']
                })
            elif story['role'] == 'user':
                processed_history.append({
                    'role' : 'user',
                    'content' : story['text']
                })
        
        processed_history.append({
            'role' : 'user',
            'content' : user_prompt
        })

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=processed_history,
        )
        
        return response.choices[0].message.content
