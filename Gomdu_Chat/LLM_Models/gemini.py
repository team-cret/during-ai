import google.generativeai as genai
import os

class GeminiLLMModel:
    def __init__(self) -> None:
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        self.generativeModel = genai.GenerativeModel('gemini-pro')

    def generateText(self, userPrompt):
        return self.generativeModel.generate_content(userPrompt)