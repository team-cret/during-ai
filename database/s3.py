from PIL import Image
import os
import io
import logging

import boto3
from botocore.exceptions import NoCredentialsError
import uuid

from setting.logger_setting import logger_setting
from setting.service_config import ServiceConfig
from setting.config import Config
from model.data_model import ReportRequest

class S3:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ[Config.AWS_ACCESS_KEY.value],
            aws_secret_access_key=os.environ[Config.AWS_SECRET_KEY.value],
        )
        logger_setting()
        self.logger = logging.getLogger(__name__)
    
    def upload_image_file(self, image:Image, report_request:ReportRequest) -> str:
        try:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format=image.format)  # 이미지의 원래 포맷 사용 (예: 'JPEG', 'PNG')
            img_byte_arr.seek(0)
            object_name = f"{report_request.couple_id}/{str(uuid.uuid4())}.png"
            self.s3.put_object(
                Bucket=ServiceConfig.S3_BUCKET_NAME.value, 
                Key=object_name, 
                Body=img_byte_arr, 
                ContentType=f'image/{image.format.lower()}'
            )

            # 업로드한 파일의 URL 생성
            file_url = f"https://{ServiceConfig.S3_BUCKET_NAME.value}.s3.amazonaws.com/{object_name}"
            
            return file_url
        
        except Exception as e:
            self.logger.error(f"Error in uploading image file: {str(e)}", exc_info=True)
            raise Exception(f"Error in uploading image file: {str(e)}")
