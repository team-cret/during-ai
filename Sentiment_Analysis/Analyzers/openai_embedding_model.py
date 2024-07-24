from langchain_openai import OpenAIEmbeddings
import numpy as np

class OpenAIEmbeddingModel:
    def __init__(self, embededSentiments):
        self.embeddingModel = OpenAIEmbeddings()
        self.embededSentiments = embededSentiments
        self.threshold = 0.5

    def analyzeSentimentByChat(self, chatData):
        embededChatDataVector = self.getEmbeddingVector(chatData)
        mostSimilarity = 0
        mostSimilarSentiment = '없음'

        for sentiment, vector in self.embededSentiments.items():
            similarity = self.calculateSimilarity(embededChatDataVector, vector)
            if similarity > mostSimilarity and similarity > self.threshold:
                mostSimilarity = similarity
                mostSimilarSentiment = sentiment
        
        return (mostSimilarSentiment, mostSimilarity)
    
    def getEmbeddingVector(self, chatData):
        return self.embeddingModel.embed_query(chatData)
    
    def calculateSimilarity(self, v1, v2):
        return np.dot(v1, v2)