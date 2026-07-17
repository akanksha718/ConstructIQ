from sqlalchemy.orm import Session

from app.models.incident import Incident


class MaintenanceAnalyzer:

    @staticmethod
    def get_equipment_history(

        db: Session,

        equipment_id: int,

    ):

        return (

            db.query(Incident)

            .filter(

                Incident.equipment_id == equipment_id

            )

            .order_by(

                Incident.incident_date.desc()

            )

            .all()

        )

    @staticmethod
    def count_failures(

        db: Session,

        equipment_id: int,

    ):

        return (

            db.query(Incident)

            .filter(

                Incident.equipment_id == equipment_id

            )

            .count()

        )