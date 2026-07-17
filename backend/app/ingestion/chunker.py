"""Self-contained industrial document chunker.

Splits parsed markdown/plain text into overlapping chunks while tracking the
current page (from ``<!-- page:N -->`` markers emitted by the parsers) and the
nearest markdown heading, so retrieval can cite page + section.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

PAGE_MARKER = re.compile(r"<!--\s*page:(\d+)\s*-->")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


@dataclass
class ParsedChunk:
    page_content: str
    page: int | None = None
    heading: str = ""
    section: str = ""
    metadata: dict = field(default_factory=dict)


class IndustrialChunker:

    def __init__(self, chunk_size: int = 1200, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_chunks(self, text: str) -> list[ParsedChunk]:
        if not text or not text.strip():
            return []

        blocks = self._blocks_with_context(text)
        return self._pack(blocks)

    def _blocks_with_context(self, text: str) -> list[dict]:
        """Split into paragraph blocks annotated with page + heading."""

        page = None
        heading = ""
        blocks: list[dict] = []
        buffer: list[str] = []

        def flush() -> None:
            content = "\n".join(buffer).strip()
            if content:
                blocks.append(
                    {"text": content, "page": page, "heading": heading}
                )
            buffer.clear()

        for line in text.splitlines():
            marker = PAGE_MARKER.search(line)
            if marker:
                flush()
                page = int(marker.group(1))
                continue

            head = HEADING.match(line.strip())
            if head:
                flush()
                heading = head.group(2).strip()
                continue

            if not line.strip():
                flush()
                continue

            buffer.append(line)

        flush()
        return blocks

    def _pack(self, blocks: list[dict]) -> list[ParsedChunk]:
        chunks: list[ParsedChunk] = []
        current: list[str] = []
        size = 0
        page = None
        heading = ""

        def emit() -> None:
            content = "\n\n".join(current).strip()
            if content:
                chunks.append(
                    ParsedChunk(
                        page_content=content,
                        page=page,
                        heading=heading,
                        section=heading,
                        metadata={"page": page, "heading": heading},
                    )
                )

        for block in blocks:
            text = block["text"]
            if not current:
                page = block["page"]
                heading = block["heading"]

            # Hard-split blocks larger than the chunk size.
            for piece in self._split_long(text):
                if size + len(piece) > self.chunk_size and current:
                    emit()
                    tail = self._overlap_tail(current)
                    current = [tail] if tail else []
                    size = len(tail)
                    page = block["page"]
                    heading = block["heading"]
                current.append(piece)
                size += len(piece)

        emit()
        return chunks

    def _split_long(self, text: str) -> list[str]:
        if len(text) <= self.chunk_size:
            return [text]

        pieces: list[str] = []
        sentences = re.split(r"(?<=[.!?])\s+", text)
        buf = ""
        for sentence in sentences:
            if len(buf) + len(sentence) > self.chunk_size and buf:
                pieces.append(buf.strip())
                buf = ""
            if len(sentence) > self.chunk_size:
                for i in range(0, len(sentence), self.chunk_size):
                    pieces.append(sentence[i : i + self.chunk_size])
                continue
            buf += (" " if buf else "") + sentence
        if buf.strip():
            pieces.append(buf.strip())
        return pieces

    def _overlap_tail(self, current: list[str]) -> str:
        joined = "\n\n".join(current)
        if len(joined) <= self.chunk_overlap:
            return joined
        return joined[-self.chunk_overlap :]
