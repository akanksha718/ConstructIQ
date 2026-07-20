"""Optional mirroring of the knowledge graph into Neo4j.

The source of truth is Postgres (``document_entities`` / ``graph_relationships``
/ ``equipment``). When Neo4j is configured, ``sync`` mirrors a document's
equipment links so graph-native queries/visualisations are possible. When it is
not configured this is a no-op.
"""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.graph.neo4j_client import Neo4jClient
from app.models.equipment import Equipment
from app.models.equipment_document import EquipmentDocument
from app.models.entity import DocumentEntity
from app.models.relationship import GraphRelationship
from app.graph.entity_resolver import EntityResolver

logger = logging.getLogger(__name__)


class KnowledgeGraphService:

    @staticmethod
    def sync(db: Session, document) -> None:
        client = Neo4jClient()
        if not client.enabled():
            return

        try:
            client.execute(
                "MERGE (d:Document {id:$id}) SET d.filename=$filename",
                id=document.id,
                filename=document.filename,
            )

            links = (
                db.query(Equipment)
                .join(
                    EquipmentDocument,
                    EquipmentDocument.equipment_id == Equipment.id,
                )
                .filter(EquipmentDocument.document_id == document.id)
                .all()
            )

            for equipment in links:
                client.execute(
                    "MERGE (e:Equipment {tag:$tag})",
                    tag=equipment.tag,
                )
                client.execute(
                    """
                    MATCH (e:Equipment {tag:$tag})
                    MATCH (d:Document {id:$id})
                    MERGE (d)-[:MENTIONS]->(e)
                    """,
                    tag=equipment.tag,
                    id=document.id,
                )

            # Mirror all extracted entities, not just equipment. This preserves
            # failure modes, standards and causes as graph-native evidence.
            entities = (
                db.query(DocumentEntity)
                .filter(DocumentEntity.document_id == document.id)
                .all()
            )
            for entity in entities:
                client.execute(
                    """
                    MERGE (e:Entity {id:$id})
                    SET e.value=$value, e.normalized=$normalized,
                        e.type=$type, e.confidence=$confidence
                    WITH e
                    MATCH (d:Document {id:$document_id})
                    MERGE (d)-[:MENTIONS]->(e)
                    """,
                    id=entity.id,
                    value=entity.entity_value,
                    normalized=EntityResolver.normalize(entity.entity_value),
                    type=entity.entity_type,
                    confidence=entity.confidence,
                    document_id=document.id,
                )

            relationships = (
                db.query(GraphRelationship)
                .join(DocumentEntity, GraphRelationship.source_entity_id == DocumentEntity.id)
                .filter(DocumentEntity.document_id == document.id)
                .all()
            )
            for relationship in relationships:
                client.execute(
                    """
                    MATCH (source:Entity {id:$source_id})
                    MATCH (target:Entity {id:$target_id})
                    MERGE (source)-[r:RELATED_TO {id:$id}]->(target)
                    SET r.type=$type, r.confidence=$confidence
                    """,
                    id=relationship.id,
                    source_id=relationship.source_entity_id,
                    target_id=relationship.target_entity_id,
                    type=relationship.relationship_type,
                    confidence=relationship.confidence,
                )
        finally:
            client.close()
