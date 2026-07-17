"""P&ID / engineering-drawing parsing.

Full symbol/line detection (computer vision) is a roadmap item. For now we OCR
any embedded text (tag numbers, legends, notes) so drawings still contribute
searchable equipment tags to the knowledge graph.
"""

from __future__ import annotations

from pathlib import Path

from app.parsers.ocr import OCRService


class PIDParser:

    def parse(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()

        if ext in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            text = OCRService.extract(file_path)
            return text or ""

        # .dwg/.dxf vector drawings require a CAD reader; not yet supported.
        return ""
