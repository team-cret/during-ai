import sentiment_analysis_keyword_analyzer as kwaz
import sentiment_analyzer_preprocessor as ppcs
from Analyzers.huggingface_facebook_bart_large_mnli import HuggingfaceFacebookBartLargeMnliAnalyzer


class AutoSentimentAnalyzer:
    def __init__(self) -> None:
        self.preprocessor = ppcs.SentimentAnalyzerPreprocessor()
        self.keywordAnalyzer = kwaz.KeywordAnalyzer(self.preprocessor.sentiments, self.preprocessor.sentimentIds)

        self.setAnalyzers()
        self.selectCurrentAnalyzer()
    
    # 현재 최신 버전의 Analyzer를 선택해주는 함수
    def selectCurrentAnalyzer(self):
        self.analyzerName = 'huggingface_facebook_bart_large_mnli'
        self.currentAnalyzer = self.analyzer[self.analyzerName]

    # 가능한 Analyzer Setting
    def setAnalyzers(self):
        self.analyzer = {
            'huggingface_facebook_bart_large_mnli' : {
                'type' : 'classification', 
                'model' : HuggingfaceFacebookBartLargeMnliAnalyzer()
            },
            'openai_embedding_model' : {
                'type' : 'embedding', 
                'model' : 'a'
            },
        }

    # Chat 한개를 받아서 그 Chat에 대한 감정을 분석해주는 함수
    def analyzeSentimentByChat(self, chatData):
        if sentiment := self.keywordAnalyzer.analyzeSentimentByKeyword(chatData):
            return sentiment

        if self.currentAnalyzer['type'] == 'classification':
            sentiment = self.currentAnalyzer['model'].analyzeSentimentByChat(self.preprocessor.sentiments, chatData)
        elif self.currentAnalyzer['type'] == 'embedding':
            sentiment = self.currentAnalyzer['model'].analyzeSentimentByChat(self.preprocessor.embededValuesOfSentiments[self.analyzerName], chatData)

        return sentiment

# analyzer 동작 확인 O
# analyzer = AutoSentimentAnalyzer()
# print(analyzer.analyzeSentimentByChat('I love you'))