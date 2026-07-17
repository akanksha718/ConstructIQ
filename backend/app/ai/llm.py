"""
Backwards-compatible ``llm`` facade.

Historically modules used ``from app.ai.llm import llm`` and called
``llm.generate_content(prompt).text``. That surface is preserved here but is now
backed by the unified, gracefully-degrading :mod:`app.ai.client`.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.ai.client import ai_client


@dataclass
class LLMResponse:
    text: str


class _LLM:
    def generate_content(self, prompt: str) -> LLMResponse:
        return LLMResponse(text=ai_client.generate_text(prompt))


llm = _LLM()
