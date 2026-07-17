"""Embedding generation for chunks and queries (pgvector storage)."""

from __future__ import annotations

from app.ai.client import ai_client


class EmbeddingService:

    @staticmethod
    def embed_document(text: str) -> list[float] | None:
        return ai_client.embed(text, task_type="retrieval_document")

    @staticmethod
    def embed_query(text: str) -> list[float] | None:
        return ai_client.embed(text, task_type="retrieval_query")
