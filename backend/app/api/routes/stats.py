from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.document import Document
from app.models.entity import DocumentEntity
from app.models.equipment import Equipment
from app.models.relationship import GraphRelationship

from app.schema.stats import StatsResponse

router = APIRouter()


@router.get("", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)) -> StatsResponse:
    """
    Aggregate knowledge-base metrics for the admin dashboards.

    All values are computed live from the database so the UI always
    reflects the real state of the ingested corpus.
    """

    documents_uploaded = db.query(func.count(Document.id)).scalar() or 0
    knowledge_entities = db.query(func.count(DocumentEntity.id)).scalar() or 0
    equipment_tags = db.query(func.count(Equipment.id)).scalar() or 0
    relationships_built = (
        db.query(func.count(GraphRelationship.id)).scalar() or 0
    )

    return StatsResponse(
        documents_uploaded=documents_uploaded,
        knowledge_entities=knowledge_entities,
        equipment_tags=equipment_tags,
        relationships_built=relationships_built,
    )
