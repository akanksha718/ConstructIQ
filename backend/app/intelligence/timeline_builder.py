from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.equipment_document import EquipmentDocument
from app.models.incident import Incident


class TimelineBuilder:

    @staticmethod
    def build(
        db: Session,
        equipment_id: int,
    ):

        timeline = []

        documents = (
            db.query(Document)
            .join(
                EquipmentDocument,
                EquipmentDocument.document_id == Document.id,
            )
            .filter(
                EquipmentDocument.equipment_id == equipment_id
            )
            .all()
        )

        for doc in documents:

            timeline.append(
                {
                    "type": "document",
                    "date": doc.created_at,
                    "title": doc.filename,
                    "status": doc.processing_status.value,
                }
            )

        incidents = (
            db.query(Incident)
            .filter(
                Incident.equipment_id == equipment_id
            )
            .all()
        )

        for incident in incidents:

            timeline.append(
                {
                    "type": "incident",
                    "date": incident.incident_date,
                    "title": incident.title,
                    "severity": incident.severity,
                }
            )

        timeline.sort(
            key=lambda x: x["date"]
        )

        return timeline