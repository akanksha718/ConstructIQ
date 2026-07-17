from pydantic import BaseModel


class Citation(BaseModel):

    document: str

    page: int

    heading: str


class ChatResponse(BaseModel):

    answer: str

    confidence: float

    citations: list[Citation]

    related_documents: list[str]

    related_equipment: list[str]