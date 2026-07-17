from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index = Column(Integer, nullable=False)

    page_number = Column(Integer)

    heading = Column(String)

    section = Column(String)

    content = Column(Text, nullable=False)

    summary = Column(Text)

    keywords = Column(JSON, default=list)

    metadata = Column(JSON, default=dict)

    document = relationship(
        "Document",
        back_populates="chunks",
    )

    entities = relationship(
        "DocumentEntity",
        back_populates="chunk",
        cascade="all, delete",
    )