from sqlalchemy.orm import Session

from app.services.equipment_service import EquipmentService


class EquipmentLinker:

    @staticmethod
    def process(

        db: Session,

        extraction,

        document,

    ):

        equipment = extraction.get(

            "equipment",

            [],

        )

        for tag in equipment:

            eq = EquipmentService.get_or_create(

                db,

                tag,

            )

            EquipmentService.link_document(

                db,

                eq.id,

                document.id,

            )