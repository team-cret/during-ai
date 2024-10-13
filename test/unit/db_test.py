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
                couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value,
                start_date = datetime(2022, 1, 1),
                end_date = datetime(2022, 1, 2),
            )
        )
        print('couple chat load', '-' * 50)
        # print(data[0])
        
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
        
