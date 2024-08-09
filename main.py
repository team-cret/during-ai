from fastapi import FastAPI
from server_manager import ServerManager
from model.data_model import CoupleChat, GomduChat, Sentiment
from datetime import datetime

manager = ServerManager()

app = FastAPI()

@app.post("/api/service/sentiment_analysis")
def analyze_sentiment(chat: CoupleChat) -> Sentiment:
    return manager.sentiment_analyzer.analyze_sentiment(chat)

@app.post("/api/service/next_gomdu_message")
def generate_next_gomdu_message(chat: GomduChat):
    return manager.gomdu.generate_next_chat(chat)

# YYYY-MM-DD
@app.post('/api/service/report')
def generate_report(couple_id:str, start_date:datetime, end_date:datetime):
    return manager.report_generator.generate_report(couple_id, start_date, end_date)