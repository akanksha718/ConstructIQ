"""Vector similarity search over ``document_chunks`` using pgvector.

Falls back to keyword (ILIKE) search when embeddings are unavailable (no Gemini
key), so retrieval still returns results in degraded mode.
"""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.vectorstore.embedding_service import EmbeddingService


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_id: int
    document_name: str
    document_url: str | None
    content: str
    page: int | None
    heading: str
    section: str
    score: float  # cosine similarity in [0, 1]; 0.0 for keyword fallback


class VectorSearcher:

    @staticmethod
    def search(
        db: Session,
        query: str,
        k: int = 8,
    ) -> list[RetrievedChunk]:
        query = (query or "").strip()
        if not query:
            return []

        embedding = EmbeddingService.embed_query(query)

        if embedding is not None:
            results = VectorSearcher._vector_search(db, embedding, k)
            if results:
                return results

        return VectorSearcher._keyword_search(db, query, k)

    @staticmethod
    def _vector_search(
        db: Session,
        embedding: list[float],
        k: int,
    ) -> list[RetrievedChunk]:
        distance = DocumentChunk.embedding.cosine_distance(embedding)

        rows = (
            db.query(
                DocumentChunk,
                Document.filename,
                Document.file_url,
                distance.label("dist"),
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .filter(DocumentChunk.embedding.isnot(None))
            .order_by(distance)
            .limit(k)
            .all()
        )

        retrieved = []
        for chunk, filename, file_url, dist in rows:
            similarity = max(0.0, 1.0 - float(dist))
            retrieved.append(
                VectorSearcher._to_retrieved(
                    chunk,
                    filename,
                    file_url,
                    similarity,
                )
            )
        return retrieved

    @staticmethod
    def _keyword_search(
        db: Session,
        query: str,
        k: int,
    ) -> list[RetrievedChunk]:
        terms = [t for t in query.split() if len(t) > 2][:6] or [query]
        conditions = [DocumentChunk.content.ilike(f"%{t}%") for t in terms]

        rows = (
            db.query(DocumentChunk, Document.filename, Document.file_url)
            .join(Document, Document.id == DocumentChunk.document_id)
            .filter(or_(*conditions))
            .limit(k)
            .all()
        )

        return [
            VectorSearcher._to_retrieved(chunk, filename, file_url, 0.0)
            for chunk, filename, file_url in rows
        ]

    @staticmethod
    def _to_retrieved(
        chunk: DocumentChunk,
        filename: str,
        file_url: str | None,
        score: float,
    ) -> RetrievedChunk:
        return RetrievedChunk(
            chunk_id=chunk.id,
            document_id=chunk.document_id,
            document_name=filename,
            document_url=file_url or None,
            content=chunk.content,
            page=chunk.page_number,
            heading=chunk.heading or "",
            section=chunk.section or "",
            score=score,
        )
