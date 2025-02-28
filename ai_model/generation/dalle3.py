import openai
import requests
from PIL import Image
from io import BytesIO
from IPython.display import display

from data.ai_report_prompt import image_generation_prompt

class DallE3:
    def __init__(self) -> None:
        self.client = openai.OpenAI()
        pass

    def generate_image(self, prompt:str):
        response = self.client.images.generate(
            model= "dall-e-3",
            prompt=image_generation_prompt + prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        url = response.data[0].url
        image = requests.get(url)
        image.raise_for_status()

        img = Image.open(BytesIO(image.content))

        return img