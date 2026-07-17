from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Asset(Base):

    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    asset_tag: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True
    )

    asset_type: Mapped[str] = mapped_column(
        String(100)
    )

    name: Mapped[str] = mapped_column(
        String(255)
    )

    description: Mapped[str] = mapped_column(
        String,
        default=""
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )