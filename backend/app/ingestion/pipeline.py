"""End-to-end ingestion pipeline.

For a stored document it: downloads the file, parses it to text (PDF/OCR/Excel/
CSV/email/image), chunks it, embeds each chunk into pgvector, extracts entities +
relationships with the LLM, builds the Postgres knowledge graph, promotes/links
equipment, and optionally mirrors to Neo4j. Every AI-dependent step degrades
gracefully so ingestion completes (chunks stored, keyword-searchable) even
without a Gemini key.
"""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.graph.graph_builder import GraphBuilder
from app.graph.graph_service import KnowledgeGraphService
from app.ingestion.chunker import IndustrialChunker
from app.models.document import ProcessingStatus
from app.models.document_chunk import DocumentChunk
from app.parsers.factory import ParserFactory
from app.services.entity_extractor import EntityExtractor
from app.services.relation_extractor import RelationExtractor
from app.services.storage_service import StorageService
from app.vectorstore.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class IngestionPipeline:

    def __init__(self) -> None:
        self.chunker = IndustrialChunker()
        self.entity_extractor = EntityExtractor()
        self.relation_extractor = RelationExtractor()

    async def run(
        self,
        document,
        db: Session,
        local_file: str | None = None,
    ) -> None:
        owns_file = local_file is None
        if local_file is None:
            local_file = await StorageService.download_file(
                document.storage_path
            )

        try:
            self._process(document, db, local_file)
        finally:
            if owns_file:
                self._cleanup(local_file)

    def _process(self, document, db: Session, local_file: str) -> None:
        text = ParserFactory.parse(document.filename, local_file)

        self._set_status(db, document, ProcessingStatus.CHUNKING)
        chunks = self.chunker.create_chunks(text)

        graph = GraphBuilder(db)

        for index, chunk in enumerate(chunks):
            embedding = EmbeddingService.embed_document(chunk.page_content)

            db_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=index,
                page_number=chunk.page or 1,
                heading=chunk.heading or "",
                section=chunk.section or "",
                content=chunk.page_content,
                chunk_metadata=chunk.metadata,
                embedding=embedding,
            )
            db.add(db_chunk)
            db.flush()

            entities = self.entity_extractor.extract(chunk.page_content)
            relations = self.relation_extractor.extract(chunk.page_content)
            graph.build_for_chunk(document, db_chunk, entities, relations)

        self._set_status(db, document, ProcessingStatus.KNOWLEDGE_GRAPH)
        graph.link_equipment(document)

        db.commit()

        # Optional Neo4j mirror (no-op when not configured).
        try:
            KnowledgeGraphService.sync(db, document)
        except Exception:  # pragma: no cover - optional
            logger.exception("Neo4j sync failed (non-fatal).")

    @staticmethod
    def _set_status(db: Session, document, status: ProcessingStatus) -> None:
        document.processing_status = status
        db.add(document)
        db.flush()

    @staticmethod
    def _cleanup(local_file: str) -> None:
        import os

        try:
            if local_file and os.path.exists(local_file):
                os.remove(local_file)
        except OSError:  # pragma: no cover
            logger.warning("Could not remove temp file %s", local_file)
