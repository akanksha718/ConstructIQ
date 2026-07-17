"""RAG chat service: retrieve context, answer with Gemini, return citations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.ai.client import ai_client
from app.ai.prompts import RAG_SYSTEM_PROMPT
from app.chat.prompts import SYSTEM_PROMPT
from app.chat.response_builder import ResponseBuilder
from app.retrieval.hybrid import HybridRetriever

NO_CONTEXT_MESSAGE = (
    "I could not find sufficient information in the knowledge base to answer "
    "that. Try uploading the relevant document or rephrasing the question."
)


class ChatService:

    def __init__(self, db: Session):
        self.db = db

    def ask(self, question: str, instruction: str = "") -> dict:
        retrieval = HybridRetriever(self.db).retrieve(question)
        context = retrieval["context"]

        if not context:
            return ResponseBuilder.build(
                answer=NO_CONTEXT_MESSAGE,
                citations=[],
                confidence=0.0,
                related_equipment=retrieval["related_equipment"],
            )

        if not ai_client.available:
            # Degraded mode: return the most relevant snippets directly.
            return ResponseBuilder.build(
                answer=self._extractive_answer(context),
                citations=retrieval["citations"],
                confidence=retrieval["confidence"],
                related_equipment=retrieval["related_equipment"],
            )

        prompt = self._build_prompt(instruction, context, question)
        answer = ai_client.generate_text(prompt) or NO_CONTEXT_MESSAGE

        return ResponseBuilder.build(
            answer=answer,
            citations=retrieval["citations"],
            confidence=retrieval["confidence"],
            related_equipment=retrieval["related_equipment"],
        )

    @staticmethod
    def _build_prompt(instruction: str, context: str, question: str) -> str:
        header = f"{SYSTEM_PROMPT}\n{RAG_SYSTEM_PROMPT}"
        if instruction:
            header = f"{header}\n\nTask:\n{instruction}"
        return (
            f"{header}\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION:\n{question}\n\n"
            "Answer using only the context above and reference the bracketed "
            "source numbers where relevant."
        )

    @staticmethod
    def _extractive_answer(context: str, limit: int = 1200) -> str:
        snippet = context[:limit].strip()
        return (
            "AI generation is not configured, so here are the most relevant "
            "passages from the knowledge base:\n\n" + snippet
        )
