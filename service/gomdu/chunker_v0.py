import importlib
from datetime import datetime, timedelta
from tqdm import tqdm

from data.considered_time_word import considered_time, parse_considered_time
from database.db_security_manager import DBSecurityManager
from database.db import DB
from database.vectordb import VectorDB
from model.data_model import CoupleChat, ChunkedData, ReportRequest
from model.db_model import Chunk, ChunkedCoupleChat, ChunkedRowNumber
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
        print('success find target couple')
        self.chunked_row_numbers = self.find_chunked_row_numbers()
        print('success find chunked row numbers')
        # self.vectordb.delete_all_chunked_couple_chat()
        # self.vectordb.delete_all_chunks()
        # delete last chunk for user
        self.delete_last_chunk_for_user()
        print('success delete last chunk for user')

        self.chunk_id_num = self.vectordb.get_max_chunk_id() + 1
        self.chunked_couple_chat_id_num = self.vectordb.get_max_chunked_couple_chat_id() + 1
        self.inserting_chunked_row_numbers = []
        self.updating_chunked_row_numbers = []
        self.max_chunked_row_number = max([numbers[0] for numbers in self.chunked_row_numbers.values()]) if self.chunked_row_numbers else 1
        print('success get max chunk id and chunked couple chat id')

        for couple_id in target_couple:
            self.automatic_chunking_by_couple(couple_id)
        
        self.insert_chunked_row_number()
        self.update_chunked_row_number()
        print('success insert and update chunked row number')

    def find_target_couple(self) -> list[str]:
        return self.db.get_all_connected_couple()
    
    def find_chunked_row_numbers(self) -> dict[str, int]:
        return self.vectordb.get_chunked_row_numbers()
    
    def delete_last_chunk_for_user(self):
        chunk_ids = self.vectordb.get_last_chunks_for_couple()
        
        self.vectordb.delete_chunked_couple_chat_by_chunk_id(chunk_ids)
        self.vectordb.delete_chunk_by_chunk_id(chunk_ids)
    
    def automatic_chunking_by_couple(self, couple_id:str):
        couple_chat = self.get_couple_chat(couple_id, self.chunked_row_numbers.get(couple_id, 0))
        print('success get couple chat')
        chunked_couple_chat = self.chunk_couple_chat(couple_chat)
        print('success chunking couple chat')
        embedded_couple_chat = self.embed_chunked_couple_chat(chunked_couple_chat)
        print('success embedding couple chat')
        
        self.update_vectordb_by_couple(couple_id, embedded_couple_chat)
        if self.chunked_row_numbers.get(couple_id) is None:
            # insert chunked row number
            self.max_chunked_row_number += 1
            self.inserting_chunked_row_numbers.append(
                ChunkedRowNumber(
                    chunked_row_number_id=self.max_chunked_row_number,
                    couple_id=couple_id,
                    row_number=couple_chat[max(0, len(couple_chat) - self.chunk_num)].chat_id
                )
            )
        else:
            self.updating_chunked_row_numbers.append(
                ChunkedRowNumber(
                    chunked_row_number_id=self.chunked_row_numbers.get(couple_id),
                    couple_id=couple_id,
                    row_number=couple_chat[max(0, len(couple_chat) - 10)].chat_id
                )
            )
            # update chunked row number

    def get_couple_chat(self, couple_id:str, chunked_row_number:int) -> list[CoupleChat]:
        couple_chat_message = self.db.get_couple_chat_for_period(
            ReportRequest(
                couple_id=couple_id,
                start_date=self.MINDATE,
                end_date=self.MAXDATE,
                chunked_row_number=chunked_row_number
            ))
        
        return self.optimize_couple_chat_to_chunk(couple_chat_message)

    def optimize_couple_chat_to_chunk(self, couple_chat:list[CoupleChat]) -> list[CoupleChat]:
        for chat in couple_chat:
            for time_word in considered_time:
                if time_word not in chat.message:
                    continue
                
                replacing_time_word = parse_considered_time(chat.timestamp, time_word)
                index = chat.message.find(time_word)
                length = len(time_word)

                chat.message = chat.message[:index] + replacing_time_word + chat.message[index+length:]
                    
            chat.message = f'[{chat.user_id[:ServiceConfig.GOMDU_CHAT_USER_ID_LENGTH.value]}] : {chat.message}'
        
        return couple_chat

    def chunk_couple_chat(self, couple_chat:list[CoupleChat]) -> list[list[CoupleChat]]:
        chunked_couple_chat = []
        if len(couple_chat) == 0:
            return chunked_couple_chat
        
        for i in range(0, len(couple_chat), 10):
            chunked_couple_chat.append(couple_chat[i:min(len(couple_chat), i+10)])
        
        return chunked_couple_chat

    def embed_chunked_couple_chat(self, chunked_couple_chat:list[list[CoupleChat]]) -> list[ChunkedData]:
        embedded_couple_chat = []

        for chunk in tqdm(chunked_couple_chat):
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
    
    def insert_chunked_row_number(self) -> bool:
        self.vectordb.insert_chunked_row_numbers(self.inserting_chunked_row_numbers)
        return True
    
    def update_chunked_row_number(self) -> bool:
        self.vectordb.update_chunked_row_numbers(self.updating_chunked_row_numbers)
        return True
