import importlib
from model.data_model import GomduChat
from setting.service_config import ServiceConfig
from database.vectordb import VectorDB
from database.db import DB
from collections import deque
from data import gomdu_prompt
from model.ai_model import AIModelInfo

class ChatGenerator:
    def __init__(self) -> None:
        self.set_generator()
        self.cached_memory = deque(maxlen=ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value)
    
    def set_generator(self) -> None:
        module = importlib.import_module(f'ai_model.generation.{ServiceConfig.GOMDU_CHAT_LLM_MODULE.value}')
        llm_class = getattr(module, ServiceConfig.GOMDU_CHAT_LLM_CLASS.value)
        self.llm_model = llm_class()

        module = importlib.import_module(f'ai_model.embedding.{ServiceConfig.GOMDU_CHAT_EMBEDDING_MODULE.value}')
        embedding_class = getattr(module, ServiceConfig.GOMDU_CHAT_EMBEDDING_CLASS.value)
        self.embedding_model = embedding_class(AIModelInfo(
            model_name=ServiceConfig.GOMDU_CHAT_EMBEDDING_MODEL_NAME.value
        ))

        self.db = DB()
        self.vector_db = VectorDB()

    def generate_next_chat(self, user_data:GomduChat) -> str:
        self.get_memory(user_data)

        # embedded_chat = self.embed_text(user_data.message)
        # document = self.retrieve_document(embedded_chat)
        user_prompt, system_prompt = self.generate_prompt(user_data)
        generated_text = self.llm_model.generate_text_by_chat_bot(user_prompt, list(self.cached_memory), system_prompt)
        print(f'Generated Text: {generated_text}')
        self.cached_memory.append({
            'role' : 'user',
            'text' : user_data.message,
        })
        self.cached_memory.append({
            'role' : 'assi',
            'text' : generated_text,
        })
        return generated_text
    
    def generate_next_chat_for_stream(self, user_data:GomduChat) -> str:
        raise NotImplementedError

    def get_memory(self, user_data:GomduChat) -> str:
        if len(self.cached_memory) == 0:
            self.cached_memory += self.db.get_gomdu_history(
                user_data.couple_id,
                user_data.user_id,
                ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value - 1
            )
    
    def embed_text(self, text:str) -> list:
        return self.embedding_model.embed_text(text)
    
    def retrieve_document(self, user_data:GomduChat, embedded_chat) -> str:
        return self.vector_db.retrieve_data(user_data.couple_id, embedded_chat)
    
    def generate_prompt(self, user_data:GomduChat) -> tuple[str, str]:
        return user_data.message, gomdu_prompt.gomdu_system_prompt