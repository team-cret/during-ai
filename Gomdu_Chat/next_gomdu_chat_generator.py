from Gomdu_Chat.LLM_Models.gemini import GeminiLLMModel

class NextGomduChatGenerator:
    def __init__(self) -> None:
        self.setLLMModel()
        self.selectLLMModel()
    
    def setLLMModel(self):
        self.LLMModelNames = [
            'gemini',
            'openai',
            'llama3',
        ]

        self.embeddingModelNames = [
            'gemini',
            'openai',
            'llama3',
        ]

        self.LLMModels = {
            self.LLMModelNames[0] : GeminiLLMModel(),
            self.LLMModelNames[1] : 0,
            self.LLMModelNames[2] : 0,
        }

        self.embeddingModels = {
            self.embeddingModelNames[0] : 0,
            self.embeddingModelNames[1] : 0,
            self.embeddingModelNames[2] : 0,
        }

    def selectLLMModel(self):
        self.selectedLLMModelName = 'gemini'
        self.selectedEmbeddingModelName = 'gemini'
        self.selectedLLMModel = self.LLMModels[self.selectedLLMModelName]
        self.selectedEmbeddingModel = self.embeddingModels[self.selectedEmbeddingModelName]

    def generateNextGomduChat(self, userData: str):
        print(userData)
        memory = self.getMemoryData()
        # embeddedVector = self.currentEmbeddingModel.getEmbeddingVector(userData['message'])
        # retrievedData = self.retrieveChatDataFromVectorDB(embeddedVector)
        userPrompt = self.generatePrompt()
        generatedResult = self.selectedLLMModel.generateText(userData)
        return generatedResult.text

    def getMemoryData(self,):
        pass

    def retrieveChatDataFromVectorDB(self, embeddedVector):
        pass
    
    def generatePrompt(self):
        pass
