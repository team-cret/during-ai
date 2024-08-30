from datetime import datetime

from database.db import DB
from database.vectordb import VectorDB
from setting.service_config import ServiceConfig

class DBTester:
    def __init__(self) -> None:
        self.setup_for_test()

    def setup_for_test(self):
        self.db = DB()
        self.vectordb = VectorDB()

    def test(self):
        data = self.db.get_couple_chat_for_period(ServiceConfig.DB_TEST_COUPLE_ID.value, datetime(2022, 1, 1), datetime(2022, 1, 2))
        print('couple chat load', '-' * 50)
        for d in data:
            print(d)
        
        print('gomdu history load', '-' * 50)
        data = self.db.get_gomdu_history(ServiceConfig.DB_TEST_COUPLE_ID.value, ServiceConfig.DB_TEST_HISTORY_ID.value)

        for d in data:
            print(d)
        
        # self.vectordb.retrieve_data()
