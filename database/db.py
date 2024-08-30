from datetime import datetime

from psycopg2.extras import register_uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.data_model import CoupleChat, GomduChat
from model.db_model import CoupleChatMessage, PetChatMessage
from setting.env_setting import EnvSetting

class DB:
    def __init__(self) -> None:
        self.set_db()
    
    def set_db(self):
        DATABASE_URL = EnvSetting().db_url
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def get_couple_chat_for_period(self, couple_id:str, start_date:datetime, end_date:datetime) -> list[CoupleChat]:
        try:
            session = self.get_session()
            query = session.query(CoupleChatMessage).filter(
                CoupleChatMessage.couple_id == str(couple_id),
                CoupleChatMessage.chat_date >= start_date,
                CoupleChatMessage.chat_date <= end_date
            ).order_by(CoupleChatMessage.couple_chat_id)
            
            chat_data = query.all()

            session.close()
            chat_data = [couple_chat.parse_to_couple_chat() for couple_chat in chat_data]
            return chat_data
        except Exception as e:
            print(f"데이터베이스에서 채팅 데이터를 가져오는 중 오류 발생: {str(e)}")
            return []
    
    def get_gomdu_history(self, couple_id:str, history_id:int) -> list[GomduChat]:
        try:
            session = self.get_session()
            query = session.query(PetChatMessage).filter(
                PetChatMessage.couple_id == str(couple_id),
                PetChatMessage.pet_chat_history_id == history_id
            ).order_by(PetChatMessage.pet_chat_id)
            
            gomdu_chat_history = query.all()
            
            session.close()
            gomdu_chat_history = [gomdu_chat.parse_to_gomdu_chat() for gomdu_chat in gomdu_chat_history]
            return gomdu_chat_history
        except Exception as e:
            print(f" Gomdu chat load error: {str(e)}")
            return []