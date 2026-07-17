"""LLM-assisted maintenance recommendations over supplied context."""

from __future__ import annotations

from app.ai.client import ai_client

PROMPT = """
You are an Industrial Maintenance Expert.

Given maintenance history, incidents and equipment details, generate (markdown):
1. Recommendations
2. Preventive actions
3. Inspection schedule
4. Spare parts suggestions
"""


class RecommendationEngine:

    @staticmethod
    def generate(context: str) -> str:
        if not ai_client.available:
            return (
                "AI generation is not configured. Provided context for manual "
                "review:\n\n" + (context or "")
            )
        return ai_client.generate_text(PROMPT + "\n\n" + (context or "")) or (
            "Unable to generate recommendations from the supplied context."
        )
