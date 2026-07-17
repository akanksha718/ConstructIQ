from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base


class EquipmentDocument(Base):

    __tablename__ = "equipment_documents"

    id = Column(Integer, primary_key=True)

    equipment_id = Column(
        Integer,
        ForeignKey(
            "equipment.id",
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

    equipment = relationship(
        "Equipment",
        back_populates="documents",
    )

    document = relationship(
        "Document",
        back_populates="equipment",
    )