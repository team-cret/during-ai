from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from model.data_model import GomduChat, CoupleChat, ConnectionLog
from setting.service_config import ServiceConfig

Base = declarative_base()

class CoupleChatMessage(Base):
    __tablename__ = 'couple_chat_message'
    __table_args__ = {'schema': ServiceConfig.DB_TEST_SCHEMA_NAME.value}
    couple_chat_id = Column(Integer, primary_key=True)
    chat_type = Column(String)
    context = Column(String)
    chat_date = Column(String)
    send_member_id = Column(String)
    couple_id = Column(Integer)

    def parse_to_couple_chat(self):
        return CoupleChat(
            chat_id=self.couple_chat_id,
            chat_type=self.chat_type,
            message=self.context,
            timestamp=self.chat_date,
            user_id=str(self.send_member_id),
            couple_id=str(self.couple_id)
        )

class PetChatMessage(Base):
    __tablename__ = 'pet_chat_message'
    __table_args__ = {'schema': ServiceConfig.DB_TEST_SCHEMA_NAME.value}
    pet_chat_id = Column(Integer, primary_key=True)
    sender = Column(String)
    content = Column(String)
    chat_date = Column(String)
    member_id = Column(String)
    couple_id = Column(String)

    def parse_to_gomdu_chat(self):
        return GomduChat(
            chat_id=self.pet_chat_id,
            sender=self.sender,
            message=self.content,
            timestamp=self.chat_date,
            user_id=str(self.member_id),
            couple_id=str(self.couple_id)
        )

class Chunk(Base):
    __tablename__ = 'chunk'
    __table_args__ = {'schema': ServiceConfig.DB_TEST_SCHEMA_NAME.value}
    chunk_id = Column(Integer, primary_key=True)
    vector = Column(String)
    summary = Column(String)
    couple_id = Column(String)

class ChunkedCoupleChat(Base):
    __tablename__ = 'chunked_couple_chat'
    __table_args__ = {'schema': ServiceConfig.DB_TEST_SCHEMA_NAME.value}
    chunk_id = Column(Integer, primary_key=True)
    couple_chat_id = Column(Integer)

class MemberActivity(Base):
    __tablename__ = 'member_activity'
    __table_args__ = {'schema': ServiceConfig.DB_TEST_SCHEMA_NAME.value}
    activity_id = Column(Integer, primary_key=True)
    member_id = Column(String)
    active_type = Column(String)
    active_date = Column(String)

    def parse_to_connection_log(self):
        return ConnectionLog(
            user_id=self.member_id,
            connection_type=self.active_type,
            timestamp=self.active_date
        )

class Couple(Base):
    __tablename__ = 'couple'
    __table_args__ = {'schema': ServiceConfig.DB_TEST_SCHEMA_NAME.value}
    couple_id = Column(String, primary_key=True)
    cash_point = Column(Integer)
    strat_date = Column(String)
    end_date = Column(String)
    state = Column(String)