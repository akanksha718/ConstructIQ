from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.auth.dependencies import require_admin

from app.services.upload_service import UploadService



router = APIRouter()


from typing import List
from fastapi import UploadFile, File

@router.post("/")
async def upload_documents(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    uploaded = []

    for file in files:
        document = await UploadService.upload_document(
            db,
            file,
            user["sub"],
        )
        uploaded.append(document)

    return {
        "message":"Upload successful",
        "documents": uploaded
    }