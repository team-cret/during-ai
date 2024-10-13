from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.data_model import CoupleChat, GomduChat, ReportRequest, ConnectionLog
from model.db_model import CoupleChatMessage, PetChat, MemberActivity, Couple
from setting.env_setting import EnvSetting
from setting.service_config import ServiceConfig

class DB:
    def __init__(self) -> None:
        self.set_db()
    
    def set_db(self):
        DATABASE_URL = EnvSetting().db_url
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()

    def get_couple_chat_for_period(self, report_request:ReportRequest) -> list[CoupleChat]:
        try:
            session = self.get_session()
            query = session.query(CoupleChatMessage).filter(
                CoupleChatMessage.couple_id == str(report_request.couple_id),
                CoupleChatMessage.message_date >= report_request.start_date,
                CoupleChatMessage.message_date <= report_request.end_date
            ).order_by(CoupleChatMessage.couple_chat_message_id)
            
            chat_data = query.all()

            session.close()
            result_data = []
            for couple_chat in chat_data:
                result_data.append(couple_chat.parse_to_couple_chat())
                
            return chat_data
        except Exception as e:
            print(f"Couple chat load error: {str(e)}")
            return []
    
    def get_gomdu_history(self, couple_id:str, user_id:str) -> list[GomduChat]:
        try:
            session = self.get_session()
            query = session.query(PetChat).filter(
                PetChat.couple_id == str(couple_id),
                PetChat.member_id == str(user_id)
            ).order_by(PetChat.pet_chat_id).limit(ServiceConfig.GOMDU_CHAT_MEMORY_SIZE.value)
            
            gomdu_chat_history = query.all()
            
            session.close()
            gomdu_chat_history = [gomdu_chat.parse_to_gomdu_chat() for gomdu_chat in gomdu_chat_history]
            return gomdu_chat_history
        except Exception as e:
            print(f"Gomdu chat load error: {str(e)}")
            return []

    def get_member_activity(self, member_id:str) -> list[ConnectionLog]:
        try:
            session = self.get_session()
            query = session.query(MemberActivity).filter(
                MemberActivity.member_id == member_id
            ).order_by(MemberActivity.id)
            
            member_activities = query.all()
            
            session.close()
            member_activities = [member_activity.parse_to_connection_log() for member_activity in member_activities]
            if len(member_activities) == 0:
                return []
            return member_activities
        except Exception as e:
            print(f"Member activity load error: {str(e)}")
            return []
    
    def get_all_connected_couple(self):
        try:
            session = self.get_session()
            query = session.query(Couple).filter(
                Couple.state == 'CONNECT'
            )
            
            connected_couples = query.all()
            
            session.close()
            connected_couple_ids = [str(connected_couple.couple_id) for connected_couple in connected_couples]
            return connected_couple_ids
        except Exception as e:
            print(f"Connected Couple Id load error: {str(e)}")
            return []