
from pydantic import BaseModel

class GomduChat(BaseModel):
    user_id: str = ''
    couple_id: str = ''
    history_id: str = ''
    message: str = ''
    timestamp: int = 0