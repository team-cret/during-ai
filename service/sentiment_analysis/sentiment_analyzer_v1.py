from .sentiment_analyzer import SentimentAnalyzer

from ai_model.embedding.text_embedding import TextEmbedding

from data.sentiments import sentiment_to_id, sentiments

from model.ai_model import AIModelInfo
from model.data_model import CoupleChat, Sentiment

from setting.service_config import ServiceConfig

from service.sentiment_analysis.keyword_analyzer import KeywordAnalyzer

import importlib
import numpy as np

class SentimentAnalyzerV1(SentimentAnalyzer):
    def __init__(self) -> None:
        self.set_analyzer()
        self.keyword_analyzer = KeywordAnalyzer()
    
    def set_analyzer(self) -> None:
        self.module_names = [
            ServiceConfig.SENTIMENT_ANALYZER_V1_MODULE1.value,
            ServiceConfig.SENTIMENT_ANALYZER_V1_MODULE2.value,
            ServiceConfig.SENTIMENT_ANALYZER_V1_MODULE3.value,
        ]

        self.class_names = [
            ServiceConfig.SENTIMENT_ANALYZER_V1_CLASS1.value,
            ServiceConfig.SENTIMENT_ANALYZER_V1_CLASS2.value,
            ServiceConfig.SENTIMENT_ANALYZER_V1_CLASS3.value,
        ]

        modules = [
            importlib.import_module(f'ai_model.classification.{module_name}')
            for module_name in self.module_names
        ]

        ai_model_classes = [
            getattr(module, class_name)
            for module, class_name in zip(modules, self.class_names)
        ]
        
        self.ai_models = [
            ai_model_class(AIModelInfo())
            for ai_model_class in ai_model_classes
        ]

    def analyze_sentiment(self, chat:CoupleChat) -> Sentiment:
        if self.keyword_analyzer.is_keyword(chat.message):
            return self.keyword_analyzer.is_keyword(chat.message)
        
        classify_results = [
            ai_model.classify_text(chat.message)
            for ai_model in self.ai_models
        ]
        
        integrated_result = {}
        for classify_result in classify_results:
            for sentiment, score in zip(classify_result['sentiments'], classify_result['scores']):
                if sentiment in integrated_result:
                    integrated_result[sentiment] += score ** 2
                else:
                    integrated_result[sentiment] = score ** 2
        
        classify_result = {
            'sentiments' : [sentiment for sentiment, _ in sorted(integrated_result.items(), key=lambda x:x[1], reverse=True)],
            'scores' : [score for _, score in sorted(integrated_result.items(), key=lambda x:x[1], reverse=True)],
        }
        return {
            'sentiment': classify_result['sentiments'][0], 
            'sentiment_id': sentiment_to_id[classify_result['sentiments'][0]],
        }