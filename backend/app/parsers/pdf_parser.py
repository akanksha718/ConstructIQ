"""PDF text extraction using pypdf, with an optional OCR fallback."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class PDFParser:

    def parse(self, file_path: str) -> str:
        try:
            from pypdf import PdfReader
        except Exception:  # pragma: no cover - dependency missing
            logger.exception("pypdf not available")
            return ""

        try:
            reader = PdfReader(file_path)
        except Exception:
            logger.exception("Failed to open PDF %s", file_path)
            return ""

        pages: list[str] = []
        for index, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text() or ""
            except Exception:
                text = ""
            pages.append(f"<!-- page:{index} -->\n{text.strip()}")

        combined = "\n\n".join(pages).strip()

        # Scanned PDF (no extractable text) -> try OCR if it is available.
        if not combined.replace("<!-- page:", "").strip():
            from app.parsers.ocr import OCRService

            ocr_text = OCRService.extract_pdf(file_path)
            if ocr_text:
                return ocr_text

        return combined
