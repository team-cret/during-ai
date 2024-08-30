from datetime import datetime, timedelta

from pydantic import BaseModel

from setting.service_config import ServiceConfig

class GomduChat(BaseModel):
    chat_id: int = 0
    sender: str = 'user'
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

class ReportRequest(BaseModel):
    couple_id:str = ''
    start_date:datetime = datetime.now()
    end_date:datetime = datetime.now()

class Report(BaseModel):
    report_type:str = ''
    image:str = ''
    MBTI:str = ''
    response_time_zone: list = [0 for _ in range(round(24/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
    concurrent_time_zone: list = [0 for _ in range(round(24/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
    frequently_talked_topic: list = []
    frequently_used_emotion: list = [('', 0) for _ in range(6)]
    frequency_of_affection: float = 0
    number_of_love_words:int = 0
    sweetness_score:float = 0
    average_reply_term:timedelta = timedelta(0)

    def parse_to_json(self):
        return {
            'report_type' : self.report_type,
            'image' : self.image,
            'MBTI' : self.MBTI,
            'response_time_zone' : self.response_time_zone,
            'concurrent_time_zone' : self.concurrent_time_zone,
            'frequently_talked_topic' : self.frequently_talked_topic,
            'frequently_used_emotion' : self.frequently_used_emotion,
            'frequency_of_affection' : self.frequency_of_affection,
            'number_of_love_words' : self.number_of_love_words,
            'sweetness_score' : self.sweetness_score,
            'average_reply_term' : self.average_reply_term,
        }