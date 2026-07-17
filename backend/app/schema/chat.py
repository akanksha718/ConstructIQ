from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str


class Citation(BaseModel):

    source_index: int

    document_id: int | None = None

    document: str

    file_url: str | None = None

    page: int | None = None

    heading: str | None = None

    section: str | None = None

    excerpt: str | None = None


class ChatResponse(BaseModel):

    answer: str

    confidence: float

    citations: list[Citation]

    related_equipment: list[str] = []

    agent: str | None = None
