from fastapi import FastAPI
from server_manager import ServerManager
from model.report import Report, ReportRequest
from model.data_model import CoupleChat, GomduChat, Sentiment
from datetime import datetime

manager = ServerManager()

app = FastAPI()

@app.post("/api/service/sentiment_analysis")
def analyze_sentiment(chat: CoupleChat) -> Sentiment:
    return manager.sentiment_analyzer.analyze_sentiment(chat)

@app.post("/api/service/next_gomdu_message")
def generate_next_gomdu_message(chat: GomduChat) -> GomduChat:
    return GomduChat(
        couple_id=chat.couple_id,
        user_id=chat.user_id,
        message=manager.gomdu.generate_next_chat(chat)
    )

# YYYY-MM-DD
@app.post('/api/service/report')
def generate_report(report_request:ReportRequest) -> Report:
    return manager.report_generator.generate_report(
        report_request.couple_id,
        report_request.start_date,
        report_request.end_date
    )