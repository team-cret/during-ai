from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.data_model import CoupleChat, GomduChat
from setting.config import Config
from setting.db_config import DBConfig

class DB:
    def __init__(self) -> None:
        DATABASE_URL = DBConfig.DATABASE_URL.value
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def load_chat_data_for_period(self, couple_id:str, start_date:datetime, end_date:datetime) -> list[CoupleChat]:
        try:
            session = self.get_session()
            query = session.query(CoupleChat).filter(
                CoupleChat.couple_id == couple_id,
                CoupleChat.timestamp >= start_date,
                CoupleChat.timestamp <= end_date
            ).order_by(CoupleChat.chat_id)
            
            chat_data = query.all()

            session.close()
            return chat_data
        except Exception as e:
            print(f"데이터베이스에서 채팅 데이터를 가져오는 중 오류 발생: {str(e)}")
            return []
    
    def get_gomdu_history(self, couple_id:int, history_id:int) -> list[GomduChat]:
        try:
            session = self.get_session()
            query = session.query(GomduChat).filter(
                GomduChat.couple_id == couple_id,
                GomduChat.history_id == history_id
            ).order_by(GomduChat.chat_id)
            
            gomdu_chat_history = query.all()
            
            session.close()
            return gomdu_chat_history
        except Exception as e:
            print(f" Gomdu chat load error: {str(e)}")
            return []