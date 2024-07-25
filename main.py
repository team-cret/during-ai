from Sentiment_Analysis import sentiment_analyzer
from Gomdu_Chat import next_gomdu_chat_generator
from config import ConfigSettings
from fastapi import FastAPI
from pydantic import BaseModel

class chatData(BaseModel):
    message: str
    memberId: str
    groupId: str
    chatId: str
    historyId: str

app = FastAPI()
settings = ConfigSettings()
settings.setAPIKeys()

sentimentAnalyzer = sentiment_analyzer.AutoSentimentAnalyzer()
gomduChatGenerator = next_gomdu_chat_generator.NextGomduChatGenerator()

@app.post("/AutoSentimentAnalysis")
def analyzeSentiment(userData: chatData):
    return sentimentAnalyzer.analyzeSentimentByChat(userData.message)

@app.pos("/GomduNextChat")
def generateNextGomduChat(userData: chatData):
    return gomduChatGenerator.generateNextGomduChat(userData)