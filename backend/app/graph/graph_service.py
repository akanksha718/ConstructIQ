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
        finally:
            client.close()
