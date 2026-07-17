from pydantic import BaseModel

from typing import List


class Citation(BaseModel):

    document: str

    page: int | None = None

    section: str | None = None


class ChatResponse(BaseModel):

    answer: str

    confidence: float

    citations: List[Citation]


class ExtractionResponse(BaseModel):

    equipment: list[str] = []

    parameters: list[str] = []

    maintenance: list[str] = []

    standards: list[str] = []

    personnel: list[str] = []

    dates: list[str] = []

    relationships: list[dict] = []