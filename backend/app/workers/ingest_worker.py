import logging
import os
import time

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.document import Document
from app.models.document import ProcessingStatus

from app.services.storage_service import StorageService


logger = logging.getLogger(__name__)


class IngestWorker:
    """
    Background worker responsible for AI ingestion.

    Responsibilities
    ----------------
    1. Download file from Supabase
    2. Update processing status
    3. Run AI pipeline
    4. Mark READY or FAILED
    5. Cleanup temp files
    """

    @staticmethod
    async def process_document(
        document_id: int,
    ) -> None:

        db: Session = SessionLocal()

        local_path = None

        start_time = time.time()

        try:

            document = (
                db.query(Document)
                .filter(Document.id == document_id)
                .first()
            )

            if document is None:
                logger.error(
                    "Document %s not found",
                    document_id,
                )
                return

            logger.info(
                "Starting ingestion for %s",
                document.filename,
            )

            document.processing_status = (
                ProcessingStatus.PROCESSING
            )

            db.commit()

            # Download from Supabase
            local_path = (
                await StorageService.download_file(
                    document.storage_path
                )
            )

            # Run AI Pipeline (imported lazily so a broken/optional
            # ingestion dependency never prevents the API from booting)
            from app.ingestion.pipeline import IngestionPipeline

            await IngestionPipeline().run(
                document=document,
                db=db,
            )

            document.processing_status = (
                ProcessingStatus.READY
            )

            db.commit()

            elapsed = round(
                time.time() - start_time,
                2,
            )

            logger.info(
                "Finished processing %s in %.2f sec",
                document.filename,
                elapsed,
            )

        except Exception:

            logger.exception(
                "Pipeline failed for %s",
                document_id,
            )

            try:

                document = (
                    db.query(Document)
                    .filter(Document.id == document_id)
                    .first()
                )

                if document:

                    document.processing_status = (
                        ProcessingStatus.FAILED
                    )

                    db.commit()

            except Exception:

                db.rollback()

        finally:

            if local_path and os.path.exists(local_path):
                os.remove(local_path)

            db.close()