import google.generativeai as genai
import numpy as np
import os

class GeminiEmbeddingModel:
    def __init__(self, embededSentiments):
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
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
        return genai.embed_content(
            model='models/embedding-001',
            content=chatData,
            task_type='classification'
        )['embedding']
    
    def calculateSimilarity(self, v1, v2):
        # return np.dot(v1, v2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))