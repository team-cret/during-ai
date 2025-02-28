
from database.vectordb import VectorDB
from database.db import DB
from service.gomdu.chunker_v0 import ChunkerV0

class ChunkerTester:
    def __init__(self):
        self.setup_for_test()
    
    def setup_for_test(self):
        self.vector_db = VectorDB()
        self.db = DB()
        self.chunker = ChunkerV0()
    
    def couple_id_test(self):
        return self.db.get_all_connected_couple()
    
    def test(self):
        # couple_ids = self.couple_id_test()
        # print(len(couple_ids))
        # if len(couple_ids):
        #     print(couple_ids[0])
        
        self.chunker.automatic_chunking()
