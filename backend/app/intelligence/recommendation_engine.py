from app.ai.llm import llm


PROMPT = """
You are an Industrial Maintenance Expert.

Given:

Maintenance history

Incidents

Equipment details

Generate

1. Recommendations

2. Preventive actions

3. Inspection schedule

4. Spare parts suggestions

Return markdown.
"""


class RecommendationEngine:

    @staticmethod
    def generate(context):

        response = llm.generate_content(

            PROMPT + context

        )

        return response.text