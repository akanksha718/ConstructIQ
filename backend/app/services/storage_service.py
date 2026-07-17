from uuid import uuid4
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import HTTPException
from fastapi import UploadFile

from app.db.supabase import supabase
from app.core.config import settings


class StorageService:
    """
    Handles all Supabase Storage operations.

    Responsibilities
    ----------------
    - Upload file
    - Download file
    - Delete file
    - Generate public URL
    """

    BUCKET = settings.SUPABASE_STORAGE_BUCKET

    # Allowed file extensions
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

    # Maximum upload size (100 MB)
    MAX_FILE_SIZE = 100 * 1024 * 1024

    @classmethod
    async def upload_file(
        cls,
        file: UploadFile,
    ) -> tuple[str, str, int]:
        """
        Upload a file to Supabase Storage.

        Returns
        -------
        storage_path
        public_url
        file_size
        """

        extension = (
            Path(file.filename)
            .suffix
            .replace(".", "")
            .lower()
        )

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

        storage_path = (
            f"documents/{filename}"
        )

        result = (
            supabase.storage
            .from_(cls.BUCKET)
            .upload(
                storage_path,
                content,
                {
                    "content-type": file.content_type,
                    "upsert": False,
                },
            )
        )

        if result is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to upload file to storage.",
            )

        public_url = (
            supabase.storage
            .from_(cls.BUCKET)
            .get_public_url(storage_path)
        )

        return (
            storage_path,
            public_url,
            size,
        )

    @classmethod
    async def download_file(
        cls,
        storage_path: str,
    ) -> str:
        """
        Download a file from Supabase
        and return a temporary local path.
        """

        data = (
            supabase.storage
            .from_(cls.BUCKET)
            .download(storage_path)
        )

        suffix = Path(storage_path).suffix

        temp = NamedTemporaryFile(
            delete=False,
            suffix=suffix,
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
        """
        Delete a file from Supabase Storage.
        """

        (
            supabase.storage
            .from_(cls.BUCKET)
            .remove([storage_path])
        )

    @classmethod
    def get_public_url(
        cls,
        storage_path: str,
    ) -> str:
        """
        Return the public URL of an existing file.
        """

        return (
            supabase.storage
            .from_(cls.BUCKET)
            .get_public_url(storage_path)
        )