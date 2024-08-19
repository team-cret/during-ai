from model.data_model import CoupleChat

from service.sentiment_analysis.sentiment_analyzer_v0 import SentimentAnalyzerV0
from service.sentiment_analysis.sentiment_analyzer_v1 import SentimentAnalyzerV1
from service.sentiment_analysis.sentiment_analyzer import SentimentAnalyzer

from time import time

class SentimentAnalyzerTester:
    def __init__(self) -> None:
        self.setup_for_test()
        self.setup_test_contents()
    
    def setup_for_test(self):
        self.sentiment_analyzers = {
            'sentiment_analyzerV0' : SentimentAnalyzerV0(),
            'sentiment_analyzerV1' : SentimentAnalyzerV1(),
        }

    def setup_test_contents(self):
        self.test_contents = [
            {'contents_type' : 'text', 'content' : '오늘도 화이팅 하구 와요!'},
            {'contents_type' : 'text', 'content' : '오늘은 너무 피곤해'},
            {'contents_type' : 'text', 'content' : '사랑해'},
            {'contents_type' : 'text', 'content' : '오늘은 뭐해?'},
            {'contents_type' : 'text', 'content' : '귀여워'},
            {'contents_type' : 'text', 'content' : '알았어'},
            {'contents_type' : 'text', 'content' : '퇴근했어!'},
            {'contents_type' : 'text', 'content' : '퇴근'},
            {'contents_type' : 'text', 'content' : '퇴근!'},
            {'contents_type' : 'text', 'content' : '힣'},
            {'contents_type' : 'text', 'content' : '헿'},
            {'contents_type' : 'text', 'content' : '잉'},
            {'contents_type' : 'text', 'content' : '밍구'},
            {'contents_type' : 'text', 'content' : '오늘도 고생했어'},
            {'contents_type' : 'text', 'content' : '오늘도 고생했져'},
            {'contents_type' : 'text', 'content' : 'ㅋ'},
        ]
    
    def test(self):
        for analyzer_name, analyzer in self.sentiment_analyzers.items():
            print(f'[{analyzer_name}] sentiment analyzer test')
            analyzer: SentimentAnalyzer

            for test_content in self.test_contents:
                start_time  = time()
                if test_content['contents_type'] == 'text':
                    print(f'{test_content['content']} -> {analyzer.analyze_sentiment(
                        CoupleChat(message=test_content['content'])
                    )}' + f' elapsed time : {time() - start_time:.2f} sec')
                    