"""RAG chat service: retrieve context, answer with Gemini, return citations."""

from __future__ import annotations
from sqlalchemy.orm import Session

from app.ai.client import ai_client
from app.ai.prompts import RAG_SYSTEM_PROMPT
from app.chat.prompts import SYSTEM_PROMPT
from app.chat.response_builder import ResponseBuilder
from app.core.redis import query_cache
from app.retrieval.hybrid import HybridRetriever

NO_CONTEXT_MESSAGE = (
    "I could not find sufficient information in the knowledge base to answer "
    "that. Try uploading the relevant document or rephrasing the question."
)


class ChatService:

    def __init__(self, db: Session):
        self.db = db

    def ask(self, question: str, instruction: str = "") -> dict:
        normalized_question = " ".join(question.split())
        cached = query_cache.get_response(normalized_question, instruction)
        if cached is not None:
            return cached

        retrieval = HybridRetriever(self.db).retrieve(question)
        context = retrieval["context"]

        if not context:
            response = ResponseBuilder.build(
                answer=NO_CONTEXT_MESSAGE,
                citations=[],
                confidence=0.0,
                related_equipment=retrieval["related_equipment"],
            )
            query_cache.set_response(normalized_question, instruction, response)
            return response

        if not ai_client.available:
            # Degraded mode: return the most relevant snippets directly.
            response = ResponseBuilder.build(
                answer=self._extractive_answer(context),
                citations=retrieval["citations"],
                confidence=HybridRetriever.confidence_for_chunks(retrieval["chunks"]),
                related_equipment=retrieval["related_equipment"],
            )
            query_cache.set_response(normalized_question, instruction, response)
            return response

        prompt = self._build_prompt(instruction, context, question)
        result = ai_client.generate_json(prompt, raise_on_error=True)
        answer = result.get("answer") if isinstance(result, dict) else None
        used = result.get("sources", []) if isinstance(result, dict) else []

        if not isinstance(answer, str) or not answer.strip() or not isinstance(used, list):
            answer, used = NO_CONTEXT_MESSAGE, []

        selected_indices = []
        for source_index in used:
            if (
                isinstance(source_index, int)
                and 1 <= source_index <= len(retrieval["citations"])
                and source_index not in selected_indices
            ):
                selected_indices.append(source_index)

        # Do not return an uncited model answer. A source-free answer is only
        # useful as an explicit "not found" response.
        if not selected_indices:
            answer = NO_CONTEXT_MESSAGE

        # One card per document page prevents adjacent chunks from producing
        # repeated citations while retaining the first chunk Gemini selected.
        citations = []
        citation_locations = set()
        selected_chunks = []
        for source_index in selected_indices:
            citation = retrieval["citations"][source_index - 1]
            location = (citation["document_id"], citation["page"])
            if location in citation_locations:
                continue
            citation_locations.add(location)
            citations.append(citation)
            selected_chunks.append(retrieval["chunks"][source_index - 1])

        response = ResponseBuilder.build(
            answer=answer,
            citations=citations,
            confidence=HybridRetriever.confidence_for_chunks(selected_chunks),
            related_equipment=retrieval["related_equipment"],
        )
        query_cache.set_response(normalized_question, instruction, response)
        return response

    @staticmethod
    def _build_prompt(instruction: str, context: str, question: str) -> str:
        header = f"{SYSTEM_PROMPT}\n{RAG_SYSTEM_PROMPT}"
        if instruction:
            header = f"{header}\n\nTask:\n{instruction}"
        return f"""
{header}

You are a grounded Retrieval-Augmented Generation (RAG) assistant.

You MUST answer ONLY from the provided context.

Each context chunk begins with a source number like:

[1]
...

[2]
...

Return ONLY valid JSON.

{{
    "answer": "your answer here",
    "sources": [1, 3]
}}

Rules:

1. Use ONLY the supplied context.
2. Never invent facts.
3. Include ONLY the source numbers that actually support your answer.
4. If the answer cannot be found, return:

{{
    "answer": "I could not find enough information in the uploaded documents.",
    "sources": []
}}

CONTEXT

{context}

QUESTION

{question}
"""

    @staticmethod
    def _extractive_answer(context: str) -> str:
        return (
            "AI generation is currently unavailable. "
            "Please see the supporting document excerpts below."
        )
