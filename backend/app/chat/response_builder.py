"""Builds the standard chat response payload."""

from __future__ import annotations


class ResponseBuilder:

    @staticmethod
    def build(
        answer: str,
        citations: list[dict],
        confidence: float,
        related_equipment: list[str] | None = None,
    ) -> dict:
        return {
            "answer": answer,
            "confidence": confidence,
            "citations": citations,
            "related_equipment": related_equipment or [],
        }
