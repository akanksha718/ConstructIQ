from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


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


class FileType(str, Enum):
    PDF = "PDF"
    DOC = "DOC"
    DOCX = "DOCX"
    PPT = "PPT"
    PPTX = "PPTX"
    XLS = "XLS"
    XLSX = "XLSX"
    CSV = "CSV"
    TXT = "TXT"
    PNG = "PNG"
    JPG = "JPG"
    JPEG = "JPEG"
    DWG = "DWG"
    DXF = "DXF"
    EML = "EML"
    MSG = "MSG"
    ZIP = "ZIP"
    OTHER = "OTHER"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    filename: Mapped[str] = mapped_column(
        String(500)
    )

    storage_path: Mapped[str] = mapped_column(
        String(500)
    )

    file_url: Mapped[str] = mapped_column(
        String(1000),
        default=""
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    file_type: Mapped[FileType] = mapped_column(
        SQLEnum(FileType),
        default=FileType.OTHER
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
        back_populates="document",
        cascade="all, delete-orphan"
    )

    equipment = relationship(
        "EquipmentDocument",
        back_populates="document",
    )
