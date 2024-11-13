from datetime import datetime, timedelta

from pydantic import BaseModel

from setting.service_config import ServiceConfig

# CoupleChat
#---------------------------------------------------#
class CoupleChat(BaseModel):
    chat_id: int = 0
    chat_type:str = ''
    message: str = ''
    user_id: str = ''
    couple_id: str = ''
    timestamp: datetime = datetime.now()
#---------------------------------------------------#

# Motion
#---------------------------------------------------#
class Motion(BaseModel):
    motion: str = ''
    motion_id: int = 0

class MotionJson(BaseModel):
    motion_id: int
#---------------------------------------------------#

# Gomdu
#---------------------------------------------------#
class GomduChat(BaseModel):
    sender: int = 0 # 0:user, 1:gomdu
    message: str = ''
    user_id: str = ''
    couple_id: str = ''

class GomduChatResponse(BaseModel):
    message:str = ''

class GomduHistoryId(BaseModel):
    couple_id:str = ''
    user_id:str = ''

class GomduReWritingQuery(BaseModel):
    query:str
#---------------------------------------------------#

# Vector DB
#---------------------------------------------------#
class RetrievedData(BaseModel):
    chunk_id: int = 0
    summary: str = ''
    similarity: float = 0
    original_message: str = ''
    couple_chat_ids: list[int] = []

class ChunkedData(BaseModel):
    chunk_id: int = 0
    chunk: str = ''
    vector: list[float] = []
    couple_chat_ids: list[int] = []
#---------------------------------------------------#

# Report
#---------------------------------------------------#
class ReportRequest(BaseModel):
    couple_id:str = ''
    start_date:datetime = datetime.now()
    end_date:datetime = datetime.now()
    couple_member_ids:list[str] = []
    chunked_row_number: int = 0

class Report(BaseModel):
    report_type:str = 'DEFAULT'
    image:str = ''
    MBTI:list[tuple[str, str]] = [('31415926-5358-9792-6535-897932384626', 'INTP'), ('43383279-5028-8419-7169-399375105820', 'ESFJ')]
    response_time_zone: list = [0 for _ in range(round(1440/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
    concurrent_time_zone: list = [0 for _ in range(round(1440/ServiceConfig.REPORT_RESPONSE_TIME_ZONE_UNIT.value))]
    frequently_talked_topic: list = []
    frequently_used_emotion: list = []
    frequency_of_affection: timedelta = timedelta(0)
    number_of_love_words:int = 0
    sweetness_score:int = 0
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

class AIReportAnalyzeResponse(BaseModel):
    MBTI:str
    frequently_talked_topic:str
    sweetness_score:int

class AIReportMainEventResponse(BaseModel):
    main_event:str
#---------------------------------------------------#

# Basic
#---------------------------------------------------#
class DeletionResult(BaseModel):
    is_success:bool = False

class ConnectionLog(BaseModel):
    user_id:str = ''
    timestamp:datetime = datetime.now()
    connection_type:str = ServiceConfig.DB_CONNECTION_LOGIN.value # LOGIN, LOGOUT
#---------------------------------------------------#