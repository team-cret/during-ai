
from pydantic import BaseModel
import datetime

class GomduChat(BaseModel):
    user_id: str = ''
    couple_id: str = ''
    history_id: str = ''
    message: str = ''
    timestamp: int = 0

class CoupleChat(BaseModel):
    chat_id: int = 0
    chat_type:str = ''
    message: str = ''
    user_id: str = ''
    couple_id: str = ''
    timestamp: datetime.datetime = datetime.datetime.now()

class Sentiment(BaseModel):
    sentiment: str = ''
    sentiment_id: int = 0