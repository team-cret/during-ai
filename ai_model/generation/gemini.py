import google.generativeai as genai
import os

class GeminiTextGenerator:
    def __init__(self, model_name:str) -> None:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        self._generative_model = genai.GenerativeModel(model_name)

    def generateText(self, userPrompt:str, systemPrompt:str) -> str:
        return self._generative_model.generate_content(userPrompt)