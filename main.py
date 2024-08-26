from fastapi import FastAPI, Request
from server_manager import ServerManager
from model.report import Report, ReportRequest
from model.data_model import CoupleChat, GomduChat, Sentiment

manager = ServerManager()

app = FastAPI()
import time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

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
