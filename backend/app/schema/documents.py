from datetime import datetime

from pydantic import BaseModel


class DocumentResponse(BaseModel):

    id: int

    filename: str

    file_type: str

    file_size: int

    processing_status: str

    storage_path: str

    file_url: str

    created_at: datetime

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):

    message: str

    documents: list[DocumentResponse]
