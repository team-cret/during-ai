from .sentiment_analysis_keyword_analyzer import KeywordAnalyzer
from .sentiment_analyzer_preprocessor import SentimentAnalyzerPreprocessor
from .Analyzers.huggingface_facebook_bart_large_mnli import HuggingfaceFacebookBartLargeMnliAnalyzer
from .Analyzers.openai_embedding_model import OpenAIEmbeddingModel
from .Analyzers.upstage_embedding_model import UpstageEmbeddingModel
from .Analyzers.huggingface_jhgan_ko_sroberta_multitask_model import HuggingfaceJhganKoSrobertaMultitaskEmbeddingModel
from .Analyzers.gemini_embedding_model import GeminiEmbeddingModel

class AutoSentimentAnalyzer:
    def __init__(self) -> None:
        self.preprocessor = SentimentAnalyzerPreprocessor()
        self.keywordAnalyzer = KeywordAnalyzer(self.preprocessor.sentiments, self.preprocessor.sentimentIds)

        self.setAnalyzers()
        self.selectCurrentAnalyzer()
    
    def selectCurrentAnalyzer(self):
        self.analyzerName = 'gemini_embedding_model'
        self.currentAnalyzer = self.analyzer[self.analyzerName]

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
            },
            'huggingface_jhgan_ko_sroberta_multitask_model' : {
                'type' : 'embedding', 
                'model' : HuggingfaceJhganKoSrobertaMultitaskEmbeddingModel(self.preprocessor.embededValuesOfSentiments['huggingface_jhgan_ko_sroberta_multitask_model'])
            },
            'gemini_embedding_model' : {
                'type' : 'embedding', 
                'model' : GeminiEmbeddingModel(self.preprocessor.embededValuesOfSentiments['gemini_embedding_model'])
            } ,
        }

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