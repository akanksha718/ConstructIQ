from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.dependencies import require_admin
from app.models.document import Document
from app.services.storage_service import StorageService

router = APIRouter()


class DocumentAccessResponse(BaseModel):
    url: str


class DocumentListItem(BaseModel):
    id: int
    filename: str
    file_type: str
    file_size: int
    processing_status: str
    uploaded_by: str
    created_at: str


def _document_access_url(document: Document) -> str:
    return StorageService.get_access_url(document.storage_path, document.file_url)


@router.get("/{document_id}/access-url", response_model=DocumentAccessResponse)
def get_document_access_url(document_id: int, db: Session = Depends(get_db)):
    """Create an access URL for a cited file, including private storage buckets."""
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    try:
        url = _document_access_url(document)
    except Exception:
        raise HTTPException(status_code=502, detail="Unable to prepare the document for viewing.")
    if not url:
        raise HTTPException(status_code=404, detail="Document file is unavailable.")
    return DocumentAccessResponse(url=url)


@router.get("/{document_id}/open", include_in_schema=False)
def open_document(document_id: int, db: Session = Depends(get_db)):
    """Redirect a cited document through the API so stale relative URLs do not break."""
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    try:
        url = _document_access_url(document)
    except Exception:
        raise HTTPException(status_code=502, detail="Unable to prepare the document for viewing.")
    if not url:
        raise HTTPException(status_code=404, detail="Document file is unavailable.")
    return RedirectResponse(url=url, status_code=307)


@router.get("", response_model=list[DocumentListItem])
def list_documents(
    db: Session = Depends(get_db),
    limit: int = Query(default=100, ge=1, le=250),
    offset: int = Query(default=0, ge=0),
    user=Depends(require_admin),
):
    """List uploaded documents for the admin asset library."""
    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return [
        DocumentListItem(
            id=document.id,
            filename=document.filename,
            file_type=document.file_type.value,
            file_size=document.file_size,
            processing_status=document.processing_status.value,
            uploaded_by=document.uploaded_by,
            created_at=document.created_at.isoformat(),
        )
        for document in documents
    ]


@router.get("/recent")
def get_recent_documents(
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    documents = (
        db.query(Document)
        .order_by(Document.created_at.desc())
        .limit(4)
        .all()
    )

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "processing_status": doc.processing_status.value,
        }
        for doc in documents
    ]
