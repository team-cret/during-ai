from fastapi import FastAPI

app = FastAPI()

@app.post("/AutoSentimentAnalysis")
def analyzeSentiment(userData: chatData):
    return sentimentAnalyzer.analyzeSentimentByChat(userData.message)

@app.post("/GomduNextChat")
def generateNextGomduChat(userData: chatData):
    return gomduChatGenerator.generateNextGomduChat(userData.message)