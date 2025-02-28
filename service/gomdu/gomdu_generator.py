from collections import deque

from database.db import DB
from database.vectordb import VectorDB
from setting.service_config import ServiceConfig

class GomduGenerator:
    def __init__(self, llm, embedding, reranker) -> None:
        self.set_gomdu(llm, embedding, reranker)

    def set_gomdu(self, llm, embedding, reranker) -> None:
        self.llm = llm
        self.embedding = embedding
        self.reranekr = reranker
        self.db = DB()
        self.vector_db = VectorDB()
        self.memory = deque(maxlen=ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value)
