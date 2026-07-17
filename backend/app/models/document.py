from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base
from sqlalchemy.orm import relationship

class ProcessingStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    METADATA = "METADATA"
    CLASSIFICATION = "CLASSIFICATION"
    CHUNKING = "CHUNKING"
    ENTITY_EXTRACTION = "ENTITY_EXTRACTION"
    KNOWLEDGE_GRAPH = "KNOWLEDGE_GRAPH"
    EMBEDDING = "EMBEDDING"
    READY = "READY"
    FAILED = "FAILED"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(300)
    )

    original_filename: Mapped[str] = mapped_column(
        String(500)
    )

    storage_path: Mapped[str] = mapped_column(
        String(500)
    )

    mime_type: Mapped[str] = mapped_column(
        String(120)
    )

    size: Mapped[int] = mapped_column(
        Integer
    )

    uploaded_by: Mapped[str] = mapped_column(
        String(100)
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        SQLEnum(ProcessingStatus),
        default=ProcessingStatus.QUEUED
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )

    entities = relationship(
        "DocumentEntity",
        cascade="all, delete-orphan"
    )
    chunks = relationship(
    "DocumentChunk",
    back_populates="document",
    cascade="all, delete",
    )
    equipment = relationship(
        "EquipmentDocument",
        back_populates="document",
    )