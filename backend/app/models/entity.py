from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base


class DocumentEntity(Base):

    __tablename__ = "document_entities"

    id = Column(Integer, primary_key=True)

    chunk_id = Column(
        Integer,
        ForeignKey(
            "document_chunks.id",
            ondelete="CASCADE",
        ),
    )

    document_id = Column(
        Integer,
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
    )

    entity_type = Column(String)

    entity_value = Column(String)

    confidence = Column(Float)

    chunk = relationship(
        "DocumentChunk",
        back_populates="entities",
    )

    relationships = relationship(
        "GraphRelationship",
        back_populates="source_entity",
        foreign_keys="GraphRelationship.source_entity_id",
    )
    relationships_incoming = relationship(
    "GraphRelationship",
    foreign_keys="GraphRelationship.target_entity_id",
    )