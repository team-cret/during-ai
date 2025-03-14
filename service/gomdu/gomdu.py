from cachetools import TTLCache
from collections import deque
import importlib
import logging

from langfuse.decorators import observe

from database.db import DB
from database.vectordb import VectorDB
from model.data_model import GomduChat, RetrievedData, GomduChatResponse
from setting.service_config import ServiceConfig
from setting.logger_setting import logger_setting

class Gomdu:
    def __init__(self) -> None:
        self.set_gomdu()
        self.generators = {}
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def set_gomdu(self) -> None:
        # llm, embedding, reranker setting
        module = importlib.import_module(f'ai_model.generation.{ServiceConfig.GOMDU_CHAT_LLM_MODULE.value}')
        self.llm_class = getattr(module, ServiceConfig.GOMDU_CHAT_LLM_CLASS.value)

        module = importlib.import_module(f'ai_model.embedding.{ServiceConfig.GOMDU_CHAT_EMBEDDING_MODULE.value}')
        self.embedding_class = getattr(module, ServiceConfig.GOMDU_CHAT_EMBEDDING_CLASS.value)

        module = importlib.import_module(f'ai_model.reranker.{ServiceConfig.GOMDU_CHAT_RERANKER_MODULE.value}')
        self.reranker_class = getattr(module, ServiceConfig.GOMDU_CHAT_RERANKER_CLASS.value)

    def make_new_generator(self, chat:GomduChat) -> None:
        try:
            self.generators[(chat.user_id, chat.couple_id)] = TTLCache(maxsize=12, ttl=ServiceConfig.GOMDU_CHAT_TTL.value)
            
            generator = self.generators[(chat.user_id, chat.couple_id)]
            generator['is_making'] = False
            generator['llm'] = self.llm_class()
            generator['embedding'] = self.embedding_class()
            generator['reranker'] = self.reranker_class()
            generator['db'] = DB()
            generator['vector_db'] = VectorDB()
            generator['memory'] = deque(maxlen=ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value)
        except Exception as e:
            self.logger.error(f"Error in making new generator: {str(e)}", exc_info=True)
            raise Exception("Error in making new generator")

    @observe
    def generate_chat(self, chat:GomduChat) -> str:
        try:
            if (chat.user_id, chat.couple_id) not in self.generators or 'is_making' not in self.generators[(chat.user_id, chat.couple_id)]:
                self.make_new_generator(chat)

            generator = self.generators[(chat.user_id, chat.couple_id)]
            if generator['is_making']:
                raise Exception('Chat is being generated')
            generator['is_making'] = True

            # memory loading
            if len(generator['memory']) == 0:
                self.get_memory(chat, generator)
            generator['memory'].append({'role' : ServiceConfig.GOMDU_CHAT_USER_NAME.value, 'text' : chat.message})
            
            # retrieval
            retrieved_data = self.retrieve_data(chat, generator)

            # prompt generation
            user_prompt, retrieved_prompt = self.generate_prompt(chat, retrieved_data)

            # llm chat generation
            gomdu_response = generator['llm'].generate_text_chat_mode(
                chat.user_id,
                user_prompt,
                retrieved_prompt,
                list(generator['memory']), 
                ServiceConfig.GOMDU_CHAT_STREAM_MODE.value
            )

            # memory reset
            generator['memory'].append({'role' : ServiceConfig.GOMDU_CHAT_AI_NAME.value, 'text' : gomdu_response})

            generator['is_making'] = False
            return GomduChatResponse(
                message = gomdu_response,
            )
        except Exception as e:
            self.logger.error(f"Error in generating chat: {str(e)}", exc_info=True)
            raise Exception("Error in generating chat")

    def get_memory(self, chat:GomduChat, generator:dict) -> None:
        try:
            gomdu_history = generator['db'].get_gomdu_history(
                chat.couple_id,
                chat.user_id,
            )
            for gomdu_chat in gomdu_history:
                generator['memory'].append({
                    'role' : gomdu_chat.sender,
                    'text' : gomdu_chat.message
                })
        except Exception as e:
            self.logger.error(f"Error in getting memory: {str(e)}", exc_info=True)
            raise Exception("Error in getting memory")

    def retrieve_data(self, chat:GomduChat, generator:dict) -> list[RetrievedData]:
        try:
            query = self.query_rewriting(generator)
            embedded_chat = self.embed_text(query, generator)
            # retrieval optimization
            db_retrieved_data = generator['vector_db'].retrieve_data(chat.couple_id, embedded_chat)

            # reranking algorithm
            # from time import time
            # start_time = time()
            # reranked_data = self.rerank_data(db_retrieved_data, generator, chat)
            reranked_data = db_retrieved_data
            # print('elpsed time :', time() - start_time
            return reranked_data
        except Exception as e:
            self.logger.error(f"Error in retrieving data: {str(e)}", exc_info=True)
            raise Exception("Error in retrieving data")
    
    def query_rewriting(self, generator:dict) -> str:
        try:
            return generator['llm'].get_retrieval_query(list(generator['memory'])).query
        except Exception as e:
            self.logger.error(f"Error in query rewriting: {str(e)}", exc_info=True)
            raise Exception("Error in query rewriting")
        
    def embed_text(self, message:str, generator:dict) -> list:
        try:
            return generator['embedding'].embed_text(message)
        except Exception as e:
            self.logger.error(f"Error in embedding text: {str(e)}", exc_info=True)
            raise Exception("Error in embedding text")
    
    def rerank_data(self, retrieved_data:list[RetrievedData], generator:dict, chat:GomduChat) -> list[RetrievedData]:
        try:
            if not retrieved_data:
                return []
            reranked_data = generator['reranker'].rerank_documents(retrieved_data, chat.message)

            reordered_data = deque([])
            for i, data in enumerate(reranked_data[:ServiceConfig.RERANKER_TOP_K.value][::-1]):
                if i:
                    reordered_data.append(data)
                else:
                    reordered_data.appendleft(data)
            return list(reordered_data)
        except Exception as e:
            self.logger.error(f"Error in reranking data: {str(e)}", exc_info=True)
            raise Exception("Error in reranking data")
    
    def generate_prompt(self, chat:GomduChat, retrieved_data:list[RetrievedData]) -> str:
        try:
            return chat.message, ' '.join([data.summary for data in retrieved_data])
        except Exception as e:
            self.logger.error(f"Error in generating prompt: {str(e)}", exc_info=True)
            raise Exception("Error in generating prompt")