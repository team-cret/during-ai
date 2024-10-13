import importlib
from datetime import datetime

from database.db_security_manager import DBSecurityManager
from database.db import DB
from database.vectordb import VectorDB
from model.data_model import CoupleChat, ChunkedData, ReportRequest
from model.db_model import Chunk, ChunkedCoupleChat
from setting.service_config import ServiceConfig

class ChunkerV0:
    MINDATE = datetime(1970, 1, 1)
    MAXDATE = datetime(9999, 12, 31)
    def __init__(self):
        self.db_encryptor = DBSecurityManager()
        self.db = DB()
        self.vectordb = VectorDB()
    
        module = importlib.import_module(f'ai_model.embedding.{ServiceConfig.GOMDU_CHAT_EMBEDDING_MODULE.value}')
        self.embedding_class = getattr(module, ServiceConfig.GOMDU_CHAT_EMBEDDING_CLASS.value)
        self.embedding_model = self.embedding_class()

        self.chunk_num = 20
        self.chunk_id_num = 1
        self.chunked_couple_chat_id_num = 1
    
    def automatic_chunking(self):
        target_couple = self.find_target_couple()
        self.vectordb.delete_all_chunked_couple_chat()
        self.vectordb.delete_all_chunks()

        for couple_id in target_couple:
            self.automatic_chunking_by_couple(couple_id)
    
    def find_target_couple(self) -> list[str]:
        return self.db.get_all_connected_couple()
    
    def automatic_chunking_by_couple(self, couple_id:str):
        couple_chat = self.get_couple_chat(couple_id)
        chunked_couple_chat = self.chunk_couple_chat(couple_chat)
        embedded_couple_chat = self.embed_chunked_couple_chat(chunked_couple_chat)
        print(len(couple_chat), len(chunked_couple_chat), len(embedded_couple_chat))
        
        self.update_vectordb_by_couple(couple_id, embedded_couple_chat)

    def get_couple_chat(self, couple_id:str):
        couple_chat_message = self.db.get_couple_chat_for_period(
            ReportRequest(
                couple_id=couple_id,
                start_date=self.MINDATE,
                end_date=self.MAXDATE
            ))
        
        return [chat.parse_to_couple_chat() for chat in couple_chat_message]

    def chunk_couple_chat(self, couple_chat:list[CoupleChat]) -> list[list[CoupleChat]]:
        chunked_couple_chat = []
        if len(couple_chat) == 0:
            return chunked_couple_chat
        
        i = 0
        for i in range(len(couple_chat) // self.chunk_num):
            chunked_couple_chat.append(couple_chat[i*self.chunk_num:(i+1)*self.chunk_num])
        
        if len(couple_chat) % self.chunk_num != 0:
            chunked_couple_chat.append(couple_chat[(i+1)*self.chunk_num:])
        
        return chunked_couple_chat

    def embed_chunked_couple_chat(self, chunked_couple_chat:list[list[CoupleChat]]) -> list[ChunkedData]:
        embedded_couple_chat = []

        for chunk in chunked_couple_chat:
            merged_chat = ' '.join([chat.message for chat in chunk])
            embedded_couple_chat.append(
                ChunkedData(
                    chunk_id=self.chunk_id_num,
                    chunk=merged_chat,
                    vector=self.embedding_model.embed_text(merged_chat),
                    couple_chat_ids=[chat.chat_id for chat in chunk]
                )
            )
            self.chunk_id_num += 1
        
        return embedded_couple_chat

    def update_vectordb_by_couple(self, couple_id:str, embedded_couple_chat:list[ChunkedData]):

        chunk_couple_chat = [
            Chunk(
                chunk_id=embedded_chat.chunk_id,
                summary=self.db_encryptor.encode_message(embedded_chat.chunk),
                vector=embedded_chat.vector,
                couple_id=couple_id,
            )
            for embedded_chat in embedded_couple_chat
        ]
        self.vectordb.insert_chunks(chunk_couple_chat)

        chunked_couple_chat = []
        for embedded_chat in embedded_couple_chat:
            for chat_id in embedded_chat.couple_chat_ids:
                chunked_couple_chat.append(
                    ChunkedCoupleChat(
                        chunked_couple_chat_id=self.chunked_couple_chat_id_num,
                        chunk_id=embedded_chat.chunk_id,
                        couple_chat_message_id=chat_id
                    )
                )
                self.chunked_couple_chat_id_num += 1
        
        self.vectordb.insert_chunked_couple_chat(chunked_couple_chat)
        return True
