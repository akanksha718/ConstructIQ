import json

from pydantic import BaseModel

from app.ai.llm import llm


class QueryAnalysis(BaseModel):

    intent: str

    equipment: list[str] = []

    standards: list[str] = []

    document_types: list[str] = []

    departments: list[str] = []


PROMPT = """
You are an Industrial AI.

Analyze the user's question.

Extract:

1. Intent
2. Equipment
3. Standards
4. Departments
5. Document Types

Return ONLY JSON.
"""


class QueryAnalyzer:

    @staticmethod
    def analyze(question: str):

        response = llm.generate_content(

            PROMPT + question

        )

        return QueryAnalysis.model_validate(

            json.loads(response.text)

        )