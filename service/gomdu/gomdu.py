from collections import deque
import importlib

from database.db import DB
from database.vectordb import VectorDB
from model.data_model import GomduChat
from setting.service_config import ServiceConfig

class Gomdu:
    def __init__(self) -> None:
        self.generators = {}
    
    def set_gomdu(self) -> None:
        module = importlib.import_module(f'ai_model.generation.{ServiceConfig.GOMDU_CHAT_LLM_MODULE.value}')
        self.llm_class = getattr(module, ServiceConfig.GOMDU_CHAT_LLM_CLASS.value)

        module = importlib.import_module(f'ai_model.embedding.{ServiceConfig.GOMDU_CHAT_EMBEDDING_MODULE.value}')
        self.embedding_class = getattr(module, ServiceConfig.GOMDU_CHAT_EMBEDDING_CLASS.value)

    def make_new_generator(self, chat:GomduChat) -> None:
        self.generators[chat.user_id] = {
            'llm' : self.llm_class(),
            'embedding' : self.embedding_class(),
            'memory' : deque(maxlen=ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value),
            'db' : DB(),
            'vector_db' : VectorDB(),
        }

    def generate_chat(self, chat:GomduChat) -> str:
        if chat.user_id not in self.generators:
            self.make_new_generator(chat)

        generator = self.generators[chat.user_id]
        # memory loading
        if len(generator['memory']) == 0:
            self.get_memory(chat)
        # chat embedding
        # retrieval
        # retrieval optimization
        # reranking
        # prompt generation
        user_prompt = self.generate_prompt(chat)
        # llm chat generation
        gomdu_response = generator['llm'].generate_text_chat_mode(user_prompt, list(generator['memory']), ServiceConfig.GOMDU_CHAT_STREAM_MODE.value)
        # memory reset
        generator['memory'].append({'role' : ServiceConfig.GOMDU_CHAT_USER_NAME.value, 'text' : chat.message})
        generator['memory'].append({'role' : ServiceConfig.GOMDU_CHAT_AI_NAME.value, 'text' : gomdu_response})

        return gomdu_response

    def get_memory(self, chat:GomduChat, generator:dict) -> None:
        gomdu_history = generator['db'].get_gomdu_history(
            chat.couple_id,
            chat.user_id,
            ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value - 1
        )

        for gomdu_chat in gomdu_history:
            generator['memory'].append({
                'role' : gomdu_chat['sender'],
                'text' : gomdu_chat['message']
            })
    
    def embed_text(self, text:str) -> list:
        return self.embedding_model.embed_text(text)
    
    def retrieve_document(self, user_data:GomduChat, embedded_chat) -> str:
        return self.vector_db.retrieve_data(user_data.couple_id, embedded_chat)
    
    def generate_prompt(self, chat:GomduChat) -> str:
        return chat.message