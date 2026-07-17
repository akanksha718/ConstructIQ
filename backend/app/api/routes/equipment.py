from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.intelligence.timeline_builder import TimelineBuilder
from app.intelligence.risk_engine import RiskEngine

router = APIRouter()


@router.get("/{equipment_id}/timeline")
def equipment_timeline(

    equipment_id: int,

    db: Session = Depends(get_db),

):

    return TimelineBuilder.build(

        db,

        equipment_id,

    )


@router.get("/{equipment_id}/risk")
def equipment_risk(

    equipment_id: int,

    db: Session = Depends(get_db),

):

    return {

        "risk": RiskEngine.calculate(

            db,

            equipment_id,

        )

    }