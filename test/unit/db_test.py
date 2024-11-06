from datetime import datetime

from database.db import DB
from database.vectordb import VectorDB
from model.data_model import ReportRequest
from setting.service_config import ServiceConfig

class DBTester:
    def __init__(self) -> None:
        self.setup_for_test()

    def setup_for_test(self):
        self.db = DB()
        self.vectordb = VectorDB()

    def test(self):
        data = self.db.get_couple_chat_for_period(
            ReportRequest(
                # couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value,
                # couple_id = 'a45b2c57-30e9-407d-b7b2-2bbaec7e224d',
                couple_id = '9e6d75c4-1444-4b12-804a-756a40726b38',
                start_date = datetime(2019, 3, 28, 0, 0, 0),
                end_date = datetime(2019, 3, 28, 23, 59, 59),
                chunked_row_number = 0
            )
        )
        print('couple chat load', '-' * 50)
        print(len(data))
        
        print('gomdu history load', '-' * 50)
        data = self.db.get_gomdu_history(ServiceConfig.DB_TEST_COUPLE_ID.value, ServiceConfig.DB_TEST_USER_ID_1.value)

        for d in data:
            print(d)
        
        from random import random
        load_embedded_vector = [random() * 2 -1 for _ in range(ServiceConfig.GOMDU_CHAT_EMBEDDING_DIMENSION.value)]
        data = self.vectordb.retrieve_data(ServiceConfig.DB_TEST_COUPLE_ID.value, load_embedded_vector)
        print('retrieved data', '-' * 50)
        for d in data:
            print(d.similarity)
        
        data = self.db.get_member_activity(ServiceConfig.DB_TEST_USER_ID_1.value)
        print('member activity load', '-' * 50)
        for d in data:
            print(d)
        
        # data = self.vectordb.get_last_chunks_for_couple()
        # print('last chunks for couple', '-' * 50)
        # print(len(data))
        # for d in data:
        #     print(d.chunk_id)
        
        data = self.db.get_all_connected_couple()
        print('all connected couple', '-' * 50)
        print(len(data))
        print(data[0])
        
