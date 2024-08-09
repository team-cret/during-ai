import importlib
from setting.service_config import ServiceConfig
from .keyword_analyzer import KeywordAnalyzer
from model.data_model import CoupleChat, Sentiment
import numpy as np
from .sentiment_analyzer import SentimentAnalyzer
from data.sentiments import sentiment_to_id

class SentimentAnalyzerV0(SentimentAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
    
    def set_analyzer(self) -> None:
        self.analyzer_type = ServiceConfig.SENTIMENT_ANALYZER_V0_TYPE.value
        self.model_name = ServiceConfig.SENTIMENT_ANALYZER_V0_MODEL_NAME.value
        self.class_name = ServiceConfig.SENTIMENT_ANALYZER_V0_CLASS_NAME.value

        module = importlib.import_module(f'ai_model.{self.analyzer_type}.{self.model_name}')
        ai_model_class = getattr(module, self.class_name)
        self.ai_model = ai_model_class()

        if self.analyzer_type == 'embedding':
            self.get_embedded_sentiments()

    def analyze_sentiment(self, chat:CoupleChat) -> Sentiment:
        if self.keyword_analyzer.is_keyword(chat.message):
            return self.keyword_analyzer.is_keyword(chat.message)
        
        if self.analyzer_type == 'classification':
            classify_result = self.ai_model.classify_text(chat.message)
            
            return {
                'sentiment': classify_result['sentiments'][0], 
                'sentiment_id': sentiment_to_id[classify_result['sentiments'][0]],
            }
        elif self.analyzer_type == 'embedding':
            return self.analyze_by_embedding(chat.message)
    
    def analyze_by_embedding(self, message:str) -> Sentiment:
        embedded_chat = self.ai_model.embed_text(message)
        for embedded_sentiment in self.embedded_sentiments:
            similarity = self.similarity(embedded_chat, embedded_sentiment)
            if similarity > 0.9:
                return self.sentiments[self.embedded_sentiments.index(embedded_sentiment)]

    def similarity(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def get_embedded_sentiments(self) -> list:
        self.embedded_sentiments = self.ai_model.get_sentiments()
