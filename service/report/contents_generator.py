
from ai_model.generation.dalle3 import DallE3
from model.data_model import Report
from model.data_model import CoupleChat

class ContentsGenerator:
    def __init__(self):
        pass

    def generate_small_report(self):
        pass

    def generate_big_report(self):
        pass
    
    def generate_image(self, couple_chat:list[CoupleChat]) -> Report:
        # prompt = '채팅 내용을 보고 채팅 내용에 가장 적합한 이미지를 생성해주세요\n' + '\n'.join([f'[{chat.user_id}] : {chat.message}' for chat in couple_chat])
        prompt = '아래 대화내용을 보고 가장 먼저 떠오르는 이미지를 생성해주세요\n' + '\n'.join([f'[{chat.user_id}] : {chat.message}' for chat in couple_chat])
        img_path = self.image_generator.generate_image(prompt)

        return Report(image=img_path)