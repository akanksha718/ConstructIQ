import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


llm = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)