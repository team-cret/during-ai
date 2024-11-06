import tiktoken

from setting.service_config import ServiceConfig
from setting.model_config import ModelConfig

class TiktokenTokenizer:
    def __init__(self):
        self.tokenizer = tiktoken.encoding_for_model(ModelConfig.OPENAI_LLM_MODEL.value)
    
    def calculate_token_length(self, text):
        return len(self.tokenizer.encode(text))