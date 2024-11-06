from PIL import Image
from datetime import datetime

from database.s3 import S3
from model.data_model import ReportRequest
from setting.service_config import ServiceConfig

class S3Tester:
    def __init__(self) -> None:
        self.setup_for_test()

    def setup_for_test(self):
        self.image = ''
        self.s3 = S3()
        self.report_request = ReportRequest(
            couple_id=ServiceConfig.DB_TEST_COUPLE_ID.value,
            start_date=str(datetime(2021, 1, 1)),
            end_date=str(datetime(2021, 1, 31))
        )

    def test(self):
        self.s3.upload_image_file(self.image, self.report_request)