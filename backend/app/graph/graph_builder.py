"""Builds the Postgres-backed knowledge graph for a document.

Entities (equipment tags, parameters, regulatory refs, personnel, dates, ...)
become ``DocumentEntity`` rows and their extracted relationships become
``GraphRelationship`` rows. Equipment entities are additionally promoted into the
``equipment`` table and linked to the document so maintenance/timeline queries
work. One ``GraphBuilder`` instance is used per document run so entity
de-duplication and relationship resolution share state.
"""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.graph.entity_resolver import EntityResolver
from app.models.entity import DocumentEntity
from app.models.relationship import GraphRelationship
from app.services.equipment_service import EquipmentService

logger = logging.getLogger(__name__)


class GraphBuilder:

    def __init__(self, db: Session):
        self.db = db
        self._by_key: dict[tuple[str, str], DocumentEntity] = {}
        self._by_norm: dict[str, DocumentEntity] = {}
        self._equipment: dict[str, str] = {}

    def build_for_chunk(
        self,
        document,
        chunk,
        entities_data: dict,
        relations_data: dict,
    ) -> None:
        for ent in (entities_data or {}).get("entities", []):
            etype = str(ent.get("type", "")).upper().strip() or "UNKNOWN"
            value = str(ent.get("value", "")).strip()
            if not value:
                continue
            confidence = self._as_float(ent.get("confidence"), 0.5)
            self._add_entity(document, chunk, etype, value, confidence)
            if etype == "EQUIPMENT":
                self._equipment[EntityResolver.normalize(value)] = value

        for rel in (relations_data or {}).get("relationships", []):
            source = str(rel.get("source", "")).strip()
            target = str(rel.get("target", "")).strip()
            if not source or not target:
                continue
            rtype = str(rel.get("relation", "RELATED_TO")).strip() or "RELATED_TO"
            confidence = self._as_float(rel.get("confidence"), 0.5)
            self._add_relationship(document, source, target, rtype, confidence)

    def link_equipment(self, document) -> None:
        for value in self._equipment.values():
            equipment = EquipmentService.get_or_create(self.db, value)
            EquipmentService.link_document(
                self.db, equipment.id, document.id
            )

    # ----------------------------------------------------------- internals
    def _add_entity(
        self,
        document,
        chunk,
        entity_type: str,
        value: str,
        confidence: float,
    ) -> DocumentEntity:
        key = (entity_type, EntityResolver.normalize(value))
        if key in self._by_key:
            return self._by_key[key]

        entity = DocumentEntity(
            document_id=document.id,
            chunk_id=chunk.id if chunk is not None else None,
            entity_type=entity_type,
            entity_value=value,
            confidence=confidence,
        )
        self.db.add(entity)
        self.db.flush()

        self._by_key[key] = entity
        self._by_norm.setdefault(EntityResolver.normalize(value), entity)
        return entity

    def _resolve_entity(self, document, value: str) -> DocumentEntity:
        norm = EntityResolver.normalize(value)
        existing = self._by_norm.get(norm)
        if existing is not None:
            return existing
        return self._add_entity(document, None, "UNKNOWN", value, 0.3)

    def _add_relationship(
        self,
        document,
        source: str,
        target: str,
        relationship_type: str,
        confidence: float,
    ) -> None:
        source_entity = self._resolve_entity(document, source)
        target_entity = self._resolve_entity(document, target)

        relationship = GraphRelationship(
            source_entity_id=source_entity.id,
            target_entity_id=target_entity.id,
            relationship_type=relationship_type,
            confidence=int(max(0.0, min(1.0, confidence)) * 100),
        )
        self.db.add(relationship)

    @staticmethod
    def _as_float(value, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
