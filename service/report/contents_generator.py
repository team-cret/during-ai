from ai_model.generation.dalle3 import DallE3
from data.ai_report_prompt import image_generation_prompt
from model.data_model import Report
from model.data_model import CoupleChat

class ContentsGenerator:
    def __init__(self):
        self.dalle3 = DallE3()
        pass

    def generate_small_report(self):
        pass

    def generate_big_report(self):
        pass
    
    def generate_image(self, main_event:str) -> Report:
        try:
            image = self.dalle3.generate_image(main_event)
            return image
        except Exception as e:
            raise Exception("Error in generating image")