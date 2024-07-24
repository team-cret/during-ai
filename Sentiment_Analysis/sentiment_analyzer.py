from .sentiment_analysis_keyword_analyzer import KeywordAnalyzer
from .sentiment_analyzer_preprocessor import SentimentAnalyzerPreprocessor
from .Analyzers.huggingface_facebook_bart_large_mnli import HuggingfaceFacebookBartLargeMnliAnalyzer
from .Analyzers.openai_embedding_model import OpenAIEmbeddingModel
from .Analyzers.upstage_embedding_model import UpstageEmbeddingModel

class AutoSentimentAnalyzer:
    def __init__(self) -> None:
        self.preprocessor = SentimentAnalyzerPreprocessor()
        self.keywordAnalyzer = KeywordAnalyzer(self.preprocessor.sentiments, self.preprocessor.sentimentIds)

        self.setAnalyzers()
        self.selectCurrentAnalyzer()
    
    # 현재 최신 버전의 Analyzer를 선택해주는 함수
    def selectCurrentAnalyzer(self):
        self.analyzerName = 'upstage_embedding_model'
        self.currentAnalyzer = self.analyzer[self.analyzerName]

    # 가능한 Analyzer Setting
    def setAnalyzers(self):
        self.analyzer = {
            'huggingface_facebook_bart_large_mnli' : {
                'type' : 'classification', 
                'model' : HuggingfaceFacebookBartLargeMnliAnalyzer(self.preprocessor.sentiments)
            },
            'openai_embedding_model' : {
                'type' : 'embedding', 
                'model' : OpenAIEmbeddingModel(self.preprocessor.embededValuesOfSentiments['openai_embedding_model'])
            },
            'upstage_embedding_model' : {
                'type' : 'embedding', 
                'model' : UpstageEmbeddingModel(self.preprocessor.embededValuesOfSentiments['upstage_embedding_model'])
            }
        }

    # Chat 한개를 받아서 그 Chat에 대한 감정을 분석해주는 함수
    def analyzeSentimentByChat(self, chatData):
        if sentiment := self.keywordAnalyzer.analyzeSentimentByKeyword(chatData):
            return sentiment

        if self.currentAnalyzer['type'] == 'classification':
            sentiment, similarity = self.currentAnalyzer['model'].analyzeSentimentByChat(chatData)
        elif self.currentAnalyzer['type'] == 'embedding':
            sentiment, similarity = self.currentAnalyzer['model'].analyzeSentimentByChat(chatData)

        if sentiment == '없음':
            return (sentiment, -1)
        return (sentiment, self.preprocessor.sentimentIds[sentiment])

# analyzer 동작 확인 O
# analyzer = AutoSentimentAnalyzer()
# print(analyzer.analyzeSentimentByChat('I love you'))