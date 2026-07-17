from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.equipment_document import EquipmentDocument


class EquipmentService:

    @staticmethod
    def get_or_create(

        db: Session,

        tag: str,

        equipment_type: str = "Unknown",

    ):

        equipment = (

            db.query(Equipment)

            .filter(
                Equipment.tag == tag
            )

            .first()

        )

        if equipment:

            return equipment

        equipment = Equipment(

            tag=tag,

            equipment_type=equipment_type,

        )

        db.add(equipment)

        db.commit()

        db.refresh(equipment)

        return equipment

    @staticmethod
    def link_document(

        db: Session,

        equipment_id: int,

        document_id: int,

    ):

        link = EquipmentDocument(

            equipment_id=equipment_id,

            document_id=document_id,

        )

        db.add(link)

        db.commit()