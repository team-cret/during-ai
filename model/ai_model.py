
from pydantic import BaseModel

class AIModelInfo(BaseModel):
    api_key_name: str = ''
    ai_model_name: str = ''
    ai_model_id: str = ''