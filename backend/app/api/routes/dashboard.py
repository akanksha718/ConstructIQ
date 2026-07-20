from typing import List, Optional
 
from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
 
from app.core.database import get_db
from app.models.document import Document, ProcessingStatus
 
from pydantic import BaseModel
 
router = APIRouter()
 
 
class RecentUploadItem(BaseModel):
    id: int
    filename: str
    file_type: str
    uploaded_by: str
    created_at: str  # ISO format
    processing_status: str
    file_size: int
 
    class Config:
        orm_mode = True
 
 
class ProcessingQueueItem(BaseModel):
    id: int
    filename: str
    uploaded_by: str
    started_at: str  # ISO format (using updated_at or created_at)
    processing_status: str
 
    class Config:
        orm_mode = True
 
 
@router.get("/recent-uploads", response_model=List[RecentUploadItem])
def get_recent_uploads(
    db: Session = Depends(get_db),
    limit: int = 10,
) -> List[RecentUploadItem]:
    """Return the most recently uploaded documents."""
    rows = (
        db.query(Document)
        .order_by(desc(Document.created_at))
        .limit(limit)
        .all()
    )
    # Pydantic will convert ORM objects
    return [
        RecentUploadItem(
            id=r.id,
            filename=r.filename,
            file_type=r.file_type.value,
            uploaded_by=r.uploaded_by,
            created_at=r.created_at.isoformat(),
            processing_status=r.processing_status.value,
            file_size=r.file_size,
        )
        for r in rows
    ]
 
 
@router.get("/processing-queue", response_model=List[ProcessingQueueItem])
def get_processing_queue(
    db: Session = Depends(get_db),
    limit: int = 20,
) -> List[ProcessingQueueItem]:
     """Return documents currently being processed."""
     rows = (
         db.query(Document)
         .filter(
             Document.processing_status.notin_(
                 [ProcessingStatus.READY, ProcessingStatus.FAILED]
             )
         )
         .order_by(Document.created_at)
         .limit(limit)
         .all()
     )
     return [
         ProcessingQueueItem(
             id=r.id,
             filename=r.filename,
             uploaded_by=r.uploaded_by,
            # Use updated_at as approximation of when processing started; fallback to created_at
            started_at=(r.updated_at or r.created_at).isoformat(),
            processing_status=r.processing_status.value,
         )
         for r in rows
     ]
 
