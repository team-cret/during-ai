
from abc import ABC, abstractmethod
from model.data_model import CoupleChat, Sentiment

class SentimentAnalyzer:
    @abstractmethod
    def analyze_sentiment(self, chat:CoupleChat) -> Sentiment:
        pass