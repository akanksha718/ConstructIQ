"""Normalises entity strings so duplicates collapse in the knowledge graph."""

from __future__ import annotations

import re


class EntityResolver:

    @staticmethod
    def normalize(value: str) -> str:
        value = (value or "").upper().strip()
        value = re.sub(r"\s+", " ", value)
        return value
