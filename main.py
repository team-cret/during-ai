from Sentiment_Analysis import sentiment_analyzer
from config import ConfigSettings
from fastapi import FastAPI
from pydantic import BaseModel
import os 

class chatData(BaseModel):
    message: str

app = FastAPI()
settings = ConfigSettings()
settings.setAPIKeys()

sentimentAnalyzer = sentiment_analyzer.AutoSentimentAnalyzer()

@app.post("/AutoSentimentAnalysis")
def analyzeSentiment(userData: chatData):
    return sentimentAnalyzer.analyzeSentimentByChat(userData.message)

