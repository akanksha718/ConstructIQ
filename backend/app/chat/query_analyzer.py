from pydantic import BaseModel

from app.ai.llm import llm


class QueryAnalysis(BaseModel):

    intent: str

    equipment: list[str]

    documents: list[str]

    standards: list[str]

    dates: list[str]

    filters: dict


class QueryAnalyzer:

    def analyze(

        self,

        question: str

    ):

        structured = llm.with_structured_output(
            QueryAnalysis
        )

        prompt = f"""

Analyze this industrial question.

Question

{question}

Return structured output.

"""

        return structured.invoke(prompt)