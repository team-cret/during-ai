
from pydantic import BaseModel
import datetime

class GomduChat(BaseModel):
    user_id: str = ''
    couple_id: str = ''
    history_id: str = ''
    message: str = ''
    timestamp: int = 0

class CoupleChat(BaseModel):
    user_id: str = ''
    couple_id: str = ''
    timestamp: datetime.datetime = datetime.datetime.now()
    message: str = ''
    chat_type:str = ''