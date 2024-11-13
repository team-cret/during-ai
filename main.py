import logging
from datetime import timedelta

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from model.data_model import (Report, ReportRequest, CoupleChat, 
                              GomduChat, MotionJson, GomduHistoryId, 
                              DeletionResult, GomduChatResponse)
from setting.logger_setting import logger_setting
from setting.service_config import ServiceConfig
from server_manager import ServerManager

manager = ServerManager()
app = FastAPI()

logger_setting()
logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"input data validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "input data validation error"}
    )

@app.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "healthy"})

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
        logger.error(f"Error in motion analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="motion analysis error")

@app.post("/api/service/gomdu/chat")
def generate_gomdu_chat(chat: GomduChat) -> GomduChatResponse:
    try:
        # chat.user_id = ServiceConfig.DB_TEST_USER_ID_1.value
        # chat.couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value
        logger.info(f"Generating Gomdu chat for: {chat}")
        result = manager.gomdu.generate_chat(chat)
        logger.info(f"Gomdu chat generated: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in Gomdu chat generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="gomdu chat generation error")
    
@app.post('/api/service/report')
def generate_report(report_request: ReportRequest) -> Report:
    try:
        # chat.couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value
        logger.info(f"Generating report for request: {report_request}")
        report_request.end_date += timedelta(hours=23, minutes=59, seconds=59)
        result = manager.report_manager.generate_report(report_request)
        logger.info(f"Report generated: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in report generation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="report generation error")

@app.delete('/api/service/gomdu/chunk')
def delete_chat_in_chunk(couple_chat:CoupleChat) -> DeletionResult:
    try:
        logger.info(f"Deleting chat in chunk: {couple_chat}")
        result = manager.gomdu.delete_chat_in_chunk(couple_chat)
        logger.info(f"Chat deleted: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in chat deletion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="chat deletion error")

@app.delete('/api/service/gomdu/memory')
def delete_gomdu_memory(history_id:GomduHistoryId) -> DeletionResult:
    try:
        logger.info(f"Deleting Gomdu memory for history id: {history_id}")
        result = manager.gomdu.delete_gomdu_memory(history_id)
        logger.info(f"Gomdu memory deleted: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in memory deletion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="memory deletion error")
