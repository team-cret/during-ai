from fastapi import FastAPI, Request

from model.data_model import Report, ReportRequest, CoupleChat, GomduChat, Motion
from server_manager import ServerManager

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

@app.post("/api/service/motion-analysis")
def analyze_motion(chat: CoupleChat) -> Motion:
    return manager.motion_analyzer.analyze_motion(chat)

@app.post("/api/service/gomdu-chat")
def generate_gomdu_chat(chat: GomduChat) -> GomduChat:
    return manager.gomdu.generate_next_chat(chat)

@app.post('/api/service/report')
def generate_report(report_request:ReportRequest) -> Report:
    return manager.report_manager.generate_report(report_request)
