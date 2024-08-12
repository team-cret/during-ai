
from .sentiment_analyzer import SentimentAnalyzer

class SentimentAnalyzerV1(SentimentAnalyzer):
    def __init__(self):
        pass
    
    def set_ensemble_model(self):
        self.ai_models = {
            
        }

    def analyze_sentiment(self, chat):
        return chat