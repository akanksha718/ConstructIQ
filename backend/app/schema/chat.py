from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str


class Citation(BaseModel):

    document: str

    page: int | None = None

    heading: str | None = None


class ChatResponse(BaseModel):

    answer: str

    confidence: float

    citations: list[Citation]