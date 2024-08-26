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
            },
            {
                'role' : 'system',
                'content' : '이번에 답할 때는 커플 대화내용 중에서 [] 이 부분을 참고해서 대답해줘 이 부분을 참고해도 모르겠으면 모른다고 대답해야돼'
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
