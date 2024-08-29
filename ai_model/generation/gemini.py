import os

import google.generativeai as genai

from ai_model.generation.generation import Generation
from data.gomdu_prompt import gomdu_system_prompt
from setting.model_config import ModelConfig

class GeminiTextGenerator(Generation):
    def __init__(self) -> None:
        self.set_model()
    
    def set_model(self) -> None:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        self._generative_model = genai.GenerativeModel(
            ModelConfig.GEMINI_LLM_MODEL.value,
        )

    def generate_text(self, user_prompt:str, history:list[dict], system_prompt:str) -> str:
        return self._generative_model.generate_content([system_prompt] + user_prompt).text
    
    def generate_text_chat_mode(self, user_prompt:str, history:list[dict], system_prompt:str, is_stream:bool = False) -> str:
        # history = [{
        #     'role' : 'user',
        #     'text' : system_prompt,
        # }] + history
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
        return self.chat.send_message(user_prompt, stream=is_stream).text