from collections import deque
from datetime import datetime
import importlib

from database.db import DB
from database.vectordb import VectorDB
from model.data_model import GomduChat, RetrievedData
from setting.service_config import ServiceConfig

class Gomdu:
    def __init__(self) -> None:
        self.set_gomdu()
        self.generators = {}
    
    def set_gomdu(self) -> None:
        module = importlib.import_module(f'ai_model.generation.{ServiceConfig.GOMDU_CHAT_LLM_MODULE.value}')
        self.llm_class = getattr(module, ServiceConfig.GOMDU_CHAT_LLM_CLASS.value)

        module = importlib.import_module(f'ai_model.embedding.{ServiceConfig.GOMDU_CHAT_EMBEDDING_MODULE.value}')
        self.embedding_class = getattr(module, ServiceConfig.GOMDU_CHAT_EMBEDDING_CLASS.value)

    def make_new_generator(self, chat:GomduChat) -> None:
        self.generators[chat.history_id] = {
            'llm' : self.llm_class(),
            'embedding' : self.embedding_class(),
            'memory' : deque(maxlen=ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value),
            'db' : DB(),
            'vector_db' : VectorDB(),
        }

    def generate_chat(self, chat:GomduChat) -> str:
        if chat.history_id not in self.generators:
            self.make_new_generator(chat)

        generator = self.generators[chat.history_id]
        # memory loading
        if len(generator['memory']) == 0:
            self.get_memory(chat, generator)
        # retrieval
        retrieved_data = self.retrieve_data(chat, generator)
        # prompt generation
        user_prompt, retrieved_prompt = self.generate_prompt(chat, retrieved_data)
        # llm chat generation
        gomdu_response = generator['llm'].generate_text_chat_mode(
            user_prompt,
            retrieved_prompt,
            list(generator['memory']), 
            ServiceConfig.GOMDU_CHAT_STREAM_MODE.value
        )
        # memory reset
        generator['memory'].append({'role' : ServiceConfig.GOMDU_CHAT_USER_NAME.value, 'text' : chat.message})
        generator['memory'].append({'role' : ServiceConfig.GOMDU_CHAT_AI_NAME.value, 'text' : gomdu_response})

        return GomduChat(
            chat_id = chat.chat_id,
            sender = ServiceConfig.GOMDU_CHAT_AI_NAME.value,
            message = gomdu_response,
            user_id = chat.user_id,
            couple_id = chat.couple_id,
            timestamp = datetime.now()
        )

    def get_memory(self, chat:GomduChat, generator:dict) -> None:
        gomdu_history = generator['db'].get_gomdu_history(
            chat.couple_id,
            chat.history_id,
        )

        for gomdu_chat in gomdu_history:
            generator['memory'].append({
                'role' : gomdu_chat['sender'],
                'text' : gomdu_chat['message']
            })

    def retrieve_data(self, chat:GomduChat, generator:dict) -> list[RetrievedData]:
        embedded_chat = self.embed_text(chat, generator)
        # retrieval optimization
        db_retrieved_data = generator['vector_db'].retrieve_data(chat.couple_id, embedded_chat)

        # reranking algorithm
        reranked_data = self.rerank_data(db_retrieved_data)
        return reranked_data
    
    def embed_text(self, chat:GomduChat, generator:dict) -> list:
        return generator['embedding'].embed_text(chat.message)
    
    def rerank_data(self, retrieved_data:list[RetrievedData]) -> list[RetrievedData]:
        return retrieved_data
    
    def generate_prompt(self, chat:GomduChat, retrieved_data:list[RetrievedData]) -> str:
        return chat.message, ' '.join([data.summary for data in retrieved_data])