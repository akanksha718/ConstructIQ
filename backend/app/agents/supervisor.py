"""Routes a question to the best specialist agent.

Uses Gemini when available; otherwise falls back to keyword routing so the
copilot keeps working without AI credentials.
"""

from __future__ import annotations

from app.ai.client import ai_client
from app.ai.prompts import SUPERVISOR_PROMPT

VALID_AGENTS = {"copilot", "maintenance", "compliance", "lessons"}

_KEYWORDS = {
    "maintenance": [
        "maintenance", "repair", "failure", "breakdown", "root cause",
        "rca", "spare", "downtime", "vibration", "bearing", "overhaul",
    ],
    "compliance": [
        "compliance", "regulation", "regulatory", "audit", "factory act",
        "oisd", "peso", "iso", "standard", "statutory", "evidence",
    ],
    "lessons": [
        "incident", "near miss", "near-miss", "lesson", "recurring",
        "pattern", "non-conformance", "nonconformance", "safety event",
    ],
}


class SupervisorAgent:

    @staticmethod
    def choose(question: str) -> str:
        if ai_client.available:
            data = ai_client.generate_json(
                SUPERVISOR_PROMPT.format(question=question)
            )
            agent = str(data.get("agent", "")).strip().lower()
            if agent in VALID_AGENTS:
                return agent

        return SupervisorAgent._keyword_route(question)

    @staticmethod
    def _keyword_route(question: str) -> str:
        lowered = question.lower()
        for agent, words in _KEYWORDS.items():
            if any(word in lowered for word in words):
                return agent
        return "copilot"
