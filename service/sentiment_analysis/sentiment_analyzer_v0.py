from .sentiment_analyzer import SentimentAnalyzer

from ai_model.embedding.text_embedding import TextEmbedding

from data.sentiments import sentiment_to_id, sentiments

from model.ai_model import AIModelInfo
from model.data_model import CoupleChat, Sentiment

from setting.service_config import ServiceConfig

from service.sentiment_analysis.keyword_analyzer import KeywordAnalyzer

import importlib
import numpy as np

class SentimentAnalyzerV0(SentimentAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
    
    def set_analyzer(self) -> None:
        self.analyzer_type = ServiceConfig.SENTIMENT_ANALYZER_V0_TYPE.value
        self.module_name = ServiceConfig.SENTIMENT_ANALYZER_V0_MODULE.value
        self.class_name = ServiceConfig.SENTIMENT_ANALYZER_V0_CLASS.value
        self.ai_model_name = ServiceConfig.SENTIMENT_ANALYZER_V0_AI_MODEL_NAME.value

        module = importlib.import_module(f'ai_model.{self.analyzer_type}.{self.module_name}')
        ai_model_class = getattr(module, self.class_name)
        self.ai_model = ai_model_class(
            AIModelInfo(
                ai_model_name=self.ai_model_name,
            )
        )

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
        self.ai_model: TextEmbedding
        embedded_chat = self.ai_model.embed_text(message)

        max_similarity = 0
        max_sentiment_id = -1
        for sentiment_id, embedded_sentiment in self.embedded_sentiments.items():
            similarity = self.similarity(embedded_chat, embedded_sentiment)

            if similarity > 0.5 and max_similarity < similarity:
                max_similarity = similarity
                max_sentiment_id = sentiment_id
        if max_sentiment_id == -1:
            return Sentiment(
                sentiment='없음',
                sentiment_id=max_sentiment_id
            )
        return Sentiment(
            sentiment=sentiments[max_sentiment_id]['sentiment'],
            sentiment_id=max_sentiment_id
        )

    def similarity(self, v1, v2) -> float:
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def get_embedded_sentiments(self) -> list:
        embedded_data = np.load(f'data/embedded_data/{self.module_name}.npz')

        self.embedded_sentiments = {}
        for key, value in embedded_data.items():
            self.embedded_sentiments[int(key)] = value