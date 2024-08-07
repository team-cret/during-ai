import google.generativeai as genai
import os
from setting.model_config import ModelConfig

class GeminiTextGenerator:
    def __init__(self) -> None:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        self._generative_model = genai.GenerativeModel(ModelConfig.GEMINI_LLM_MODEL.value)

    def generate_text(self, user_prompt:str, history:list[str], system_prompt:str) -> str:
        return self._generative_model.generate_content([system_prompt] + user_prompt).text
    
    def generate_text_by_chat_bot(self, user_prompt:str, history:list[str], system_prompt:str) -> str:
        history = [{
            'role' : 'user',
            'text' : system_prompt,
        }] + history
        processed_history = []
        for story in history:
            if story['role'] == 'assi':
                processed_history.append({
                    'role' : 'model',
                    'parts' : [story['text']]
                })
            elif story['role'] == 'user':
                processed_history.append({
                    'role' : 'user',
                    'parts' : [story['text']]
                })

        self.chat = self._generative_model.start_chat(history=processed_history)
        return self.chat.send_message(user_prompt).text다음