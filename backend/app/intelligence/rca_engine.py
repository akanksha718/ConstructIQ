"""LLM-assisted Root Cause Analysis over supplied context."""

from __future__ import annotations

from app.ai.client import ai_client

PROMPT = """
You are an Industrial Root Cause Analysis Expert.

Using ONLY the supplied information, provide (in markdown):
- Root Cause
- Evidence
- Corrective Action
- Preventive Action
- Confidence
"""


class RCAEngine:

    @staticmethod
    def analyze(context: str) -> str:
        if not ai_client.available:
            return (
                "AI generation is not configured. Provided context for manual "
                "RCA:\n\n" + (context or "")
            )
        return ai_client.generate_text(PROMPT + "\n\n" + (context or "")) or (
            "Unable to generate an RCA from the supplied context."
        )
