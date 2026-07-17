from sqlalchemy.orm import Session

from app.models.entity import DocumentEntity


class GraphSearcher:

    def __init__(self, db: Session):

        self.db = db

    def search(

        self,

        equipment: list[str],

    ):

        if not equipment:

            return []

        return (

            self.db.query(DocumentEntity)

            .filter(

                DocumentEntity.entity_value.in_(

                    equipment

                )

            )

            .all()

        )