from langchain_openai import OpenAIEmbeddings

class OpenAIEmbeddingModel:
    def __init__(self, embededSentiments):
        self.embeddingModel = OpenAIEmbeddings()
        self.embededSentiments = embededSentiments

    # sentiment의 
    def analyzeSentimentByChat(self, chatData):
        embededChatDataVector = self.getEmbeddingVector(chatData)
        mostSimilarity = 0
        mostSimilarSentiment = '없음'

        for sentiment, vector in self.embededSentiments.items():
            similarity = self.calculateSimilarity(embededChatDataVector, vector)
            if similarity > mostSimilarity:
                mostSimilarity = similarity
                mostSimilarSentiment = sentiment
        
        return [mostSimilarSentiment, mostSimilarity]
    
    def getEmbeddingVector(self, chatData):
        return self.embeddingModel.embed_query(chatData)
    
    def calculateSimilarity(self, v1, v2):
        # inner product similarity
        return sum([v1[i] * v2[i] for i in range(len(v1))])
        # angular similarity
        # manhattan distance