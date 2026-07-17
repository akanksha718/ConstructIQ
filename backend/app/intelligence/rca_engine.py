from app.ai.llm import llm


PROMPT = """
You are an Industrial Root Cause Analysis Expert.

Using ONLY supplied information,

Provide

Root Cause

Evidence

Corrective Action

Preventive Action

Confidence

Return markdown.
"""


class RCAEngine:

    @staticmethod
    def analyze(context):

        response = llm.generate_content(

            PROMPT + context

        )

        return response.text