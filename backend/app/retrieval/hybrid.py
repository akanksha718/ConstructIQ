"""Hybrid retrieval: vector similarity + knowledge-graph entity expansion.

Returns the assembled context string, per-source citations (document, page,
heading) and an overall confidence derived from the best similarity score. Works
in degraded mode (keyword search) when embeddings are unavailable.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.graph.entity_resolver import EntityResolver
from app.models.entity import DocumentEntity
from app.vectorstore.search import RetrievedChunk, VectorSearcher


class HybridRetriever:

    def __init__(self, db: Session):
        self.db = db

    def retrieve(self, question: str, k: int = 8) -> dict:
        chunks = VectorSearcher.search(self.db, question, k=k)
        related_equipment = self._related_equipment(question)

        context = self._build_context(chunks)
        citations = self._build_citations(chunks)
        confidence = self._confidence(chunks)

        return {
            "context": context,
            "citations": citations,
            "confidence": confidence,
            "related_equipment": related_equipment,
        }

    def _related_equipment(self, question: str) -> list[str]:
        """Surface equipment tags mentioned in the question via the graph."""

        tokens = {
            EntityResolver.normalize(t)
            for t in question.replace(",", " ").split()
            if len(t) > 2
        }
        if not tokens:
            return []

        equipment = (
            self.db.query(DocumentEntity.entity_value)
            .filter(DocumentEntity.entity_type == "EQUIPMENT")
            .distinct()
            .all()
        )
        return [
            value
            for (value,) in equipment
            if EntityResolver.normalize(value) in tokens
        ]

    @staticmethod
    def _build_context(chunks: list[RetrievedChunk]) -> str:
        parts = []
        for index, chunk in enumerate(chunks, start=1):
            location = f"{chunk.document_name}"
            if chunk.page:
                location += f", p.{chunk.page}"
            if chunk.heading:
                location += f", {chunk.heading}"
            parts.append(f"[{index}] ({location})\n{chunk.content}")
        return "\n\n".join(parts)

    @staticmethod
    def _build_citations(chunks: list[RetrievedChunk]) -> list[dict]:
        citations = []
        for index, chunk in enumerate(chunks, start=1):
            citations.append(
                {
                    "source_index": index,
                    "document_id": chunk.document_id,
                    "document": chunk.document_name,
                    "file_url": chunk.document_url,
                    "page": chunk.page,
                    "heading": chunk.heading or None,
                    "section": chunk.section or None,
                    "excerpt": HybridRetriever._excerpt(chunk.content),
                }
            )
        return citations

    @staticmethod
    def _confidence(chunks: list[RetrievedChunk]) -> float:
        if not chunks:
            return 0.0
        top = max(c.score for c in chunks)
        return round(float(top), 3)

    @staticmethod
    def _excerpt(content: str, limit: int = 220) -> str:
        cleaned = " ".join((content or "").split())
        if len(cleaned) <= limit:
            return cleaned
        return cleaned[: limit - 3].rstrip() + "..."
