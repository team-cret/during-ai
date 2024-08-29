
from pydantic import BaseModel
from datetime import datetime

class GomduChat(BaseModel):
    chat_id: int = 0
    message: str = ''
    history_id: str = ''
    user_id: str = ''
    couple_id: str = ''
    timestamp: datetime = datetime.now()

class CoupleChat(BaseModel):
    chat_id: int = 0
    chat_type:str = ''
    message: str = ''
    user_id: str = ''
    couple_id: str = ''
    timestamp: datetime = datetime.now()

class Motion(BaseModel):
    motion: str = ''
    motion_id: int = 0

class RetrievedData(BaseModel):
    user_id: str = ''
    couple_id: str = ''
    chat_id: int = 0
    summary: str = ''
    original_message: str = ''
    couple_chat_ids: list[int] = []
    timestamp: datetime = datetime.now()