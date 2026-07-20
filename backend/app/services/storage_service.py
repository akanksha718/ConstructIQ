from uuid import uuid4
from pathlib import Path
from tempfile import NamedTemporaryFile
import logging

from fastapi import HTTPException, UploadFile

from app.db.supabase import supabase
from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """
    Handles all Supabase Storage operations.
    """

    BUCKET = settings.SUPABASE_BUCKET

    ALLOWED_EXTENSIONS = {
        "pdf",
        "doc",
        "docx",
        "ppt",
        "pptx",
        "xls",
        "xlsx",
        "csv",
        "txt",
        "png",
        "jpg",
        "jpeg",
        "dwg",
        "dxf",
        "eml",
        "msg",
        "zip",
    }

    MAX_FILE_SIZE = 100 * 1024 * 1024

    @classmethod
    async def upload_file(
        cls,
        file: UploadFile,
    ) -> tuple[str, str, int]:

        extension = Path(file.filename).suffix.lower().replace(".", "")

        if extension not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {extension}",
            )

        content = await file.read()
        size = len(content)

        if size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="File exceeds maximum allowed size (100 MB).",
            )

        filename = f"{uuid4()}.{extension}"
        storage_path = f"documents/{filename}"

        try:
            print("=" * 60)
            print("SUPABASE URL :", settings.SUPABASE_URL)
            print("BUCKET       :", cls.BUCKET)
            print("UPLOAD PATH  :", storage_path)
            print("FILE SIZE    :", size)
            print("=" * 60)

            result = (
                supabase.storage
                .from_(cls.BUCKET)
                .upload(
                    storage_path,
                    content,
                    file_options={
                        "content-type": file.content_type,
                        "upsert": "false",
                    },
                )
            )

            print("UPLOAD RESULT:", result)

            public_url = (
                supabase.storage
                .from_(cls.BUCKET)
                .get_public_url(storage_path)
            )

            print("PUBLIC URL:", public_url)

            return (
                storage_path,
                public_url,
                size,
            )

        except Exception as e:
            logger.exception("Supabase upload failed")
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    @classmethod
    async def download_file(
        cls,
        storage_path: str,
    ) -> str:

        data = (
            supabase.storage
            .from_(cls.BUCKET)
            .download(storage_path)
        )

        temp = NamedTemporaryFile(
            delete=False,
            suffix=Path(storage_path).suffix,
        )

        temp.write(data)
        temp.flush()
        temp.close()

        return temp.name

    @classmethod
    async def delete_file(
        cls,
        storage_path: str,
    ) -> None:

        supabase.storage.from_(cls.BUCKET).remove([storage_path])

    @classmethod
    def get_public_url(
        cls,
        storage_path: str,
    ) -> str:

        return (
            supabase.storage
            .from_(cls.BUCKET)
            .get_public_url(storage_path)
        )

    @classmethod
    def get_access_url(cls, storage_path: str, fallback_url: str = "") -> str:
        """Return a short-lived URL that works for both private and public buckets."""
        if not storage_path:
            return fallback_url

        try:
            result = (
                supabase.storage
                .from_(cls.BUCKET)
                .create_signed_url(storage_path, 60 * 10)
            )
            if isinstance(result, dict):
                return result.get("signedURL") or result.get("signed_url") or fallback_url
            return getattr(result, "signed_url", None) or getattr(result, "signedURL", None) or fallback_url
        except Exception:
            logger.exception("Unable to create a signed document URL for %s", storage_path)
            return fallback_url or cls.get_public_url(storage_path)
