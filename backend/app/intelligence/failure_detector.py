from sqlalchemy.orm import Session

from app.models.incident import Incident


FAILURE_KEYWORDS = [

    "failure",

    "leak",

    "corrosion",

    "vibration",

    "bearing",

    "seal",

    "temperature",

    "trip",

    "shutdown",

]


class FailureDetector:

    @staticmethod
    def detect(text: str):

        detected = []

        lower = text.lower()

        for keyword in FAILURE_KEYWORDS:

            if keyword in lower:

                detected.append(keyword)

        return detected

    @staticmethod
    def create_incident(

        db: Session,

        equipment_id: int,

        title: str,

    ):

        incident = Incident(

            equipment_id=equipment_id,

            title=title,

            severity="Unknown",

        )

        db.add(incident)

        db.commit()

        return incident