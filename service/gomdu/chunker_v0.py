from datetime import datetime

from database.db import DB
from database.vectordb import VectorDB
from model.data_model import CoupleChat, ChunkedData

class ChunkerV0:
    MINDATE = datetime(1970, 1, 1)
    MAXDATE = datetime(9999, 12, 31)
    def __init__(self):
        self.db = DB()
        self.vectordb = VectorDB()
    
    def automatic_chunking(self, couple_id:str):
        target_couple = self.find_target_couple()

        for couple_id in target_couple:
            self.automatic_chunking_by_couple(couple_id)
    
    def find_target_couple(self) -> list[str]:
        raise NotImplementedError
    
    def automatic_chunking_by_couple(self, couple_id:str):
        couple_chat = self.get_couple_chat(couple_id)
        chunked_couple_chat = self.chunk_couple_chat(couple_chat)
        embedded_couple_chat = self.embed_chunked_couple_chat(chunked_couple_chat)
        
        self.update_vectordb_by_couple(couple_id, embedded_couple_chat)

    def get_couple_chat(self, couple_id:str):
        self.db.get_couple_chat_for_period(couple_id, self.MINDATE, self.MAXDATE)

    def chunk_couple_chat(self, couple_chat:list[CoupleChat]) -> list[list[CoupleChat]]:
        raise NotImplementedError

    def embed_chunked_couple_chat(self, chunked_couple_chat:list[list[CoupleChat]]) -> list[ChunkedData]:
        raise NotImplementedError

    def update_vectordb_by_couple(self, couple_id:str, embedded_couple_chat:list[ChunkedData]):
        raise NotImplementedError
