from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from database.db_security_manager import DBSecurityManager
from model.data_model import GomduChat, CoupleChat, ConnectionLog
from setting.service_config import ServiceConfig

Base = declarative_base()

db_schema_type = {
    'test' : ServiceConfig.DB_TEST_SCHEMA_NAME.value,
    'dev' : ServiceConfig.DB_DEV_SCHEMA_NAME.value,
    'live' : ServiceConfig.DB_LIVE_SCHEMA_NAME.value,
}

db_encryptor = DBSecurityManager()

class BCoupleChatMessage(Base):
    __tablename__ = 'couple_chat_message'
    __table_args__ = {'schema': 'vectordb'}
    couple_chat_id = Column(Integer, primary_key=True)
    chat_type = Column(String)
    context = Column(String)
    chat_date = Column(String)
    send_member_id = Column(String)
    couple_id = Column(String)

    def parse_to_couple_chat(self):
        return CoupleChat(
            chat_id=self.couple_chat_id,
            chat_type=self.chat_type,
            message=self.context,
            user_id=str(self.send_member_id),
            couple_id=str(self.couple_id),
            timestamp=self.chat_date
        )

class CoupleChatMessage(Base):
    __tablename__ = 'couple_chat_message'
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    couple_chat_message_id = Column(Integer, primary_key=True)
    message_type = Column(String)
    content = Column(String)
    message_date = Column(String)
    send_member_id = Column(String)
    couple_id = Column(String)

    def parse_to_couple_chat(self):
        return CoupleChat(
            chat_id=self.couple_chat_message_id,
            chat_type=self.message_type,
            message=db_encryptor.decode_message(self.content),
            user_id=str(self.send_member_id),
            couple_id=str(self.couple_id),
            timestamp=self.message_date
        )

class PetChat(Base):
    __tablename__ = 'pet_chat'
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    pet_chat_id = Column(Integer, primary_key=True)
    sender = Column(String)
    content = Column(String)
    chat_date = Column(String)
    member_id = Column(String)
    couple_id = Column(String)

    def parse_to_gomdu_chat(self):
        return GomduChat(
            sender=self.sender,
            message=self.content,
            user_id=str(self.member_id),
            couple_id=str(self.couple_id)
        )

class Chunk(Base):
    __tablename__ = ServiceConfig.DB_RETRIEVAL_TABLE_NAME.value
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    chunk_id = Column(Integer, primary_key=True)
    vector = Column(String)
    summary = Column(String)
    couple_id = Column(String)

class ChunkedCoupleChat(Base):
    __tablename__ = 'chunked_couple_chat'
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    chunked_couple_chat_id = Column(Integer, primary_key=True)
    chunk_id = Column(Integer)
    couple_chat_message_id = Column(Integer)

class ChunkedRowNumber(Base):
    __tablename__ = 'chunked_row_number'
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    chunked_row_number_id = Column(Integer, primary_key=True)
    row_number = Column(Integer)
    couple_id = Column(String)

class MemberActivity(Base):
    __tablename__ = 'member_activity'
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    id = Column(Integer, primary_key=True)
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
    __table_args__ = {'schema': db_schema_type[ServiceConfig.DB_CURRENT_TYPE.value]}
    couple_id = Column(String, primary_key=True)
    start_date = Column(String)
    end_date = Column(String)
    state = Column(String)