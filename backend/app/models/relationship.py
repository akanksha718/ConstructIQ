from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base


class GraphRelationship(Base):

    __tablename__ = "graph_relationships"

    id = Column(Integer, primary_key=True)

    source_entity_id = Column(
        Integer,
        ForeignKey(
            "document_entities.id",
            ondelete="CASCADE",
        ),
    )

    target_entity_id = Column(
        Integer,
        ForeignKey(
            "document_entities.id",
            ondelete="CASCADE",
        ),
    )

    relationship_type = Column(String)

    confidence = Column(Integer, default=100)

    source_entity = relationship(
        "DocumentEntity",
        foreign_keys=[source_entity_id],
    )

    target_entity = relationship(
        "DocumentEntity",
        foreign_keys=[target_entity_id],
    )