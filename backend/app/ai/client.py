import json

from google import genai

from app.core.config import settings


class AIClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def generate_json(
        self,
        prompt: str
    ):

        response = self.client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "").strip()

        return json.loads(text)


ai_client = AIClient()