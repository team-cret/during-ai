
class NextGomduChatGenerator:
    def __init__(self) -> None:
        pass
    
    def setLLMModel(self):
        self.candidateLLMModelNames = [
            'gemini',
            'openai',
            'llama3',
        ]

        self.candidateLLMModels = {
            self.candidateLLMModelNames[0] : 0,
            self.candidateLLMModelNames[1] : 0,
            self.candidateLLMModelNames[2] : 0,
        }

        self.candidateEmbeddingModels = {
            self.candidateLLMModelNames[0] : 0,
            self.candidateLLMModelNames[1] : 0,
            self.candidateLLMModelNames[2] : 0,
        }

    def selectLLMModel(self):
        self.currentLLMModelName = 'gemini'
        self.currentLLMModel = self.candidateLLMModelNames[self.currentLLMModelName]
        self.currentEmbeddingModel = self.candidateEmbeddingModels[self.currentLLMModelName]

    def generateNextGomduChat(self, userData):
        memory = self.getMemoryData()
        embeddedVector = self.currentEmbeddingModel.getEmbeddingVector(userData['message'])
        retrievedData = self.retrieveChatDataFromVectorDB(embeddedVector)
        userPrompt = self.generatePrompt()
        generatedResult = self.currentLLMModel.generateText(userPrompt)
        return generatedResult

    def getMemoryData(self,):
        pass

    def retrieveChatDataFromVectorDB(self, embeddedVector):
        pass
    
    def generatePrompt(self):
        pass
