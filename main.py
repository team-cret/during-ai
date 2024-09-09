import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from model.data_model import Report, ReportRequest, CoupleChat, GomduChat, MotionJson
from setting.logger_setting import logger_setting
from server_manager import ServerManager

manager = ServerManager()
app = FastAPI()

logger_setting()
logger = logging.getLogger(__name__)

# import time
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = float(time.time() - start_time)
#     response.headers["X-Process-Time"] = str(process_time)
#     logger.info(f"Request to {request.url.path} took {process_time:.2f} seconds")
#     return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"input data validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "input data validation error"}
    )

@app.post("/api/service/motion-analysis")
def analyze_motion(chat: CoupleChat) -> MotionJson:
    try:
        logger.info(f"Analyzing motion for chat: {chat}")
        result = manager.motion_analyzer.analyze_motion(chat)
        logger.info(f"Motion analysis result: {result}")
        return MotionJson(
            motion_id=result.motion_id
        )
    except Exception as e:
        logger.error(f"Error in motion analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="motion analysis error")

@app.post("/api/service/gomdu-chat")
def generate_gomdu_chat(chat: GomduChat) -> GomduChat:
    try:
        logger.info(f"Generating Gomdu chat for: {chat}")
        result = manager.gomdu.generate_chat(chat)
        logger.info(f"Gomdu chat generated: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in Gomdu chat generation: {str(e)}")
        raise HTTPException(status_code=500, detail="gomdu chat generation error")
    
@app.post('/api/service/report')
def generate_report(report_request: ReportRequest) -> Report:
    try:
        logger.info(f"Generating report for request: {report_request}")
        result = manager.report_manager.generate_report(report_request)
        logger.info(f"Report generated: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in report generation: {str(e)}")
        raise HTTPException(status_code=500, detail="report generation error")
