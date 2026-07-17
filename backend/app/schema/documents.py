from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):

    id: int

    title: str

    status: str

    storage_path: str

    created_at: datetime

    class Config:
        from_attributes = True