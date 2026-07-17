from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector

from app.core.database import Base


class DocumentChunk(Base):

    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE"
        )
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer
    )

    page_number: Mapped[int] = mapped_column(
        Integer
    )

    heading: Mapped[str] = mapped_column(
        String(300),
        default=""
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict
    )

    embedding: Mapped[list] = mapped_column(
        Vector(768)
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )

    entities = relationship(
        "DocumentEntity",
        cascade="all, delete-orphan"
    )