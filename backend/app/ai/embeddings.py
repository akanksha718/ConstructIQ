import os

import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiEmbedding:

    MODEL = "models/text-embedding-004"

    @classmethod
    def embed(cls, text: str):

        result = genai.embed_content(

            model=cls.MODEL,

            content=text,

            task_type="retrieval_document",

        )

        return result["embedding"]