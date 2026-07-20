"""
Unified Google Gemini client for ConstructIQ.

Everything AI-related (LLM generation + embeddings) goes through this module so
the rest of the codebase never talks to the SDK directly. The client degrades
gracefully: if the ``GEMINI_API_KEY`` is missing/placeholder or the SDK is not
installed, ``available`` is ``False`` and callers fall back to deterministic,
non-AI behaviour instead of crashing. This keeps ingestion, retrieval and the
API fully importable and testable without live credentials.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from sqlalchemy import text
from typer import prompt

from app.core.config import settings

logger = logging.getLogger(__name__)

# Dimension of models/text-embedding-004 output. Must match
# DocumentChunk.embedding = Vector(EMBEDDING_DIM).
EMBEDDING_DIM = 768

_PLACEHOLDER_KEYS = {"", "d", "dummy", "changeme", "your-gemini-api-key"}

LLM_MODEL = settings.GEMINI_LLM_MODEL
EMBEDDING_MODEL = "gemini-embedding-001"


class GeminiQuotaError(RuntimeError):
    """Gemini rejected a request because the configured quota is exhausted."""


class GeminiModelError(RuntimeError):
    """The configured Gemini model is unavailable for the current API key."""


def _looks_like_placeholder(key: str | None) -> bool:
    if not key:
        return True
    return key.strip().lower() in _PLACEHOLDER_KEYS


class AIClient:
    """Thin wrapper around ``google.generativeai`` with safe fallbacks."""

    def __init__(self) -> None:
        self._genai = None
        self.available = False

        if _looks_like_placeholder(settings.GEMINI_API_KEY):
            logger.warning(
                "GEMINI_API_KEY not configured; AI features run in "
                "degraded (no-LLM) mode."
            )
            return

        try:
            from google import genai

            self._client = genai.Client(
                api_key=settings.GEMINI_API_KEY
            )

            self.available = True
        except Exception:  # pragma: no cover - optional dependency/network
            logger.exception(
                "Failed to initialise Gemini client; running in degraded mode."
            )

    # ------------------------------------------------------------------ text
    def generate_text(self, prompt: str) -> str:
        if not self.available:
            return ""

        try:
            response = self._client.models.generate_content(
                model=LLM_MODEL,
                contents=prompt,
            )
            return response.text.strip()
        except Exception:  # pragma: no cover - network
            logger.exception("Gemini text generation failed.")
            return ""

    def generate_json(
        self, prompt: str, *, raise_on_error: bool = False
    ) -> dict[str, Any]:
        """Request JSON from Gemini and return a parsed object, or an empty dict."""

        if not self.available:
            return {}

        try:
            response = self._client.models.generate_content(
                model=LLM_MODEL,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )
            return self._parse_json(response.text or "")
        except Exception as exc:  # pragma: no cover - network/SDK version
            logger.exception("Gemini JSON generation failed.")
            message = str(exc).lower()
            if raise_on_error and any(
                marker in message
                for marker in ("resource_exhausted", "quota", "rate limit", "429")
            ):
                raise GeminiQuotaError(
                    "Gemini API quota is exhausted or rate-limited. Please try again later."
                ) from exc
            if raise_on_error and any(
                marker in message for marker in ("not_found", "not found", "no longer available")
            ):
                raise GeminiModelError(
                    f"The configured Gemini model '{LLM_MODEL}' is unavailable. "
                    "Update GEMINI_LLM_MODEL in backend/.env and restart the backend."
                ) from exc
            return {}

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        if not text:
            return {}

        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-zA-Z]*", "", cleaned).strip()
            cleaned = cleaned.rstrip("`").strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            # Fall back to the first {...} block we can find.
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if not match:
                return {}
            try:
                data = json.loads(match.group(0))
            except json.JSONDecodeError:
                return {}

        return data if isinstance(data, dict) else {}

    # ------------------------------------------------------------- embeddings
    def embed(
        self,
        text: str,
        task_type: str = "retrieval_document",
    ) -> list[float] | None:
        """Return an embedding vector, or ``None`` when AI is unavailable."""

        if not self.available:
            return None

        content = (text or "").strip()
        if not content:
            return None

        try:
            result = self._client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=content,
            )
            return result.embeddings[0].values
        except Exception:  # pragma: no cover - network
            logger.exception("Gemini embedding failed.")
            return None

    def embed_query(self, text: str) -> list[float] | None:
        return self.embed(text, task_type="retrieval_query")

ai_client = AIClient()
