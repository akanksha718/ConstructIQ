from sqlalchemy.orm import Session

from app.models.document import Document


class MetadataSearcher:

    def __init__(

        self,

        db: Session,

    ):

        self.db = db

    def search(

        self,

        analysis,

    ):

        query = self.db.query(Document)

        if analysis.document_types:

            query = query.filter(

                Document.document_type.in_(

                    analysis.document_types

                )

            )

        return query.all()