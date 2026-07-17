from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy.orm import relationship

from app.core.database import Base


class Equipment(Base):

    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)

    tag = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    name = Column(String)

    equipment_type = Column(String)

    location = Column(String)

    manufacturer = Column(String)

    model = Column(String)

    description = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    documents = relationship(
        "EquipmentDocument",
        back_populates="equipment",
        cascade="all, delete",
    )

    incidents = relationship(
        "Incident",
        back_populates="equipment",
        cascade="all, delete",
    )