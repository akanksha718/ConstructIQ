from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from app.core.database import Base


class Incident(Base):

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)

    equipment_id = Column(
        Integer,
        ForeignKey(
            "equipment.id",
            ondelete="CASCADE",
        ),
    )

    title = Column(String)

    incident_date = Column(Date)

    severity = Column(String)

    root_cause = Column(Text)

    corrective_action = Column(Text)

    equipment = relationship(
        "Equipment",
        back_populates="incidents",
    )