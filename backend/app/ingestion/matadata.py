import os
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel


class DocumentMetadata(BaseModel):

    filename: str

    extension: str

    size: int

    created_at: str


class MetadataExtractor:

    @staticmethod
    def extract(file_path: str):

        path = Path(file_path)

        stat = os.stat(file_path)

        return DocumentMetadata(

            filename=path.name,

            extension=path.suffix.lower(),

            size=stat.st_size,

            created_at=datetime.fromtimestamp(
                stat.st_ctime
            ).isoformat()

        )