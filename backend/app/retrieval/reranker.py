from __future__ import annotations

import re

from app.ai.client import ai_client

class GeminiReranker:

    @staticmethod
    def rerank(question: str, chunks: list, top_k: int = 5):

        if not chunks:
            return []

        # Preserve vector/keyword order if Gemini is unavailable or returns an
        # invalid ranking. This keeps retrieval deterministic in degraded mode.
        fallback = GeminiReranker._lexical_rank(question, chunks)[:top_k]
        if not ai_client.available:
            return fallback

        context = ""

        for i, chunk in enumerate(chunks, 1):
            # Bound prompt size so one oversized document cannot make reranking
            # fail for the entire request.
            excerpt = " ".join((chunk.content or "").split())[:1800]
            context += f"""

[{i}]
{excerpt}

"""

        prompt = f"""
You are ranking retrieved chunks.

Question:

{question}

Chunks:

{context}

Return ONLY JSON.

{{
"ranking":[4,1,7,3,5]
}}

The ranking must contain the most relevant chunk numbers first.
"""

        result = ai_client.generate_json(prompt)

        order = result.get("ranking", [])
        if not isinstance(order, list):
            return fallback

        ranked = []

        seen = set()
        for index in order:
            if isinstance(index, int) and 1 <= index <= len(chunks) and index not in seen:
                ranked.append(chunks[index-1])
                seen.add(index)

        # Keep useful retrieval candidates that the model omitted, so malformed
        # partial rankings cannot accidentally discard all evidence.
        ranked.extend(chunk for chunk in fallback if chunk not in ranked)
        return ranked[:top_k] or fallback

    @staticmethod
    def _lexical_rank(question: str, chunks: list) -> list:
        """Stable local reranker used on outages and before LLM reranking."""
        terms = set(re.findall(r"[a-z0-9-]+", question.lower()))
        if not terms:
            return list(chunks)

        def score(chunk) -> tuple[float, float]:
            content = (chunk.content or "").lower()
            overlap = sum(1 for term in terms if term in content)
            # Preserve the vector rank as the deterministic tie-breaker.
            return (overlap / len(terms), float(getattr(chunk, "score", 0.0)))

        return sorted(chunks, key=score, reverse=True)
