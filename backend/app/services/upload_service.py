import asyncio
import logging
from pathlib import Path

from fastapi import HTTPException
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document import FileType
from app.models.document import ProcessingStatus

from app.services.storage_service import StorageService
from app.workers.ingest_worker import IngestWorker

logger = logging.getLogger(__name__)


class UploadService:
    """
    Handles document uploads.

    Flow
    ----
    1. Upload file to Supabase
    2. Create database record
    3. Commit transaction
    4. Start background AI ingestion
    """

    @staticmethod
    async def upload_document(
        db: Session,
        file: UploadFile,
        uploaded_by: str,
    ) -> Document:

        storage_path = None

        try:

            (
                storage_path,
                public_url,
                file_size,
            ) = await StorageService.upload_file(file)

            extension = (
                Path(file.filename)
                .suffix
                .replace(".", "")
                .upper()
            )

            try:
                file_type = FileType[extension]
            except KeyError:
                file_type = FileType.OTHER

            document = Document(
                filename=file.filename,
                storage_path=storage_path,
                file_url=public_url,
                file_size=file_size,
                file_type=file_type,
                uploaded_by=uploaded_by,
                processing_status=ProcessingStatus.QUEUED,
            )

            db.add(document)

            db.commit()

            db.refresh(document)

            logger.info(
                "Uploaded document %s (%s)",
                document.filename,
                document.id,
            )

            # Background AI processing
            asyncio.create_task(
                IngestWorker.process_document(
                    document.id,
                )
            )

            return document

        except Exception as e:

            db.rollback()

            logger.exception("Upload failed")

            # Remove uploaded file if DB transaction failed
            if storage_path:
                try:
                    await StorageService.delete_file(storage_path)
                except Exception:
                    logger.exception(
                        "Failed to clean up storage."
                    )

            if isinstance(e, HTTPException):
                raise e

            raise HTTPException(
                status_code=500,
                detail="Document upload failed.",
            )