"""Embedding helpers backed by the unified Gemini client."""

from __future__ import annotations

from app.ai.client import ai_client


class GeminiEmbedding:

    @classmethod
    def embed(cls, text: str) -> list[float] | None:
        return ai_client.embed(text)

    @classmethod
    def embed_query(cls, text: str) -> list[float] | None:
        return ai_client.embed_query(text)
