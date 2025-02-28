import logging
import logging.config
from logging.handlers import RotatingFileHandler
import pytz
from datetime import datetime
class KSTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        KST = pytz.timezone('Asia/Seoul')
        dt = datetime.fromtimestamp(record.created, KST)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()

def logger_setting():
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    '()': KSTFormatter,
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'app.log',
                    'formatter': 'default',
                    'level': 'DEBUG',
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf8',
                },
                # 'console': {
                #     'class': 'logging.StreamHandler',
                #     'formatter': 'default',
                #     'level': 'INFO',
                # },
            },
            'root': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }
    )