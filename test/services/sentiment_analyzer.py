from service.sentiment_analysis.sentiment_analyzer_v0 import SentimentAnalyzerV0

class SentimentAnalyzerTester:
    def __init__(self) -> None:
        self.sentiment_analyzer = SentimentAnalyzerV0()
    
    def test(self):
        input_data = "I am happy"
        print(self.sentiment_analyzer.analyze_sentiment(chatData=input_data))