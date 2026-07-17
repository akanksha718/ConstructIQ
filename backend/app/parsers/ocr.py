"""Optional OCR for scanned images / PDFs.

OCR depends on pytesseract + Pillow (and the system ``tesseract`` binary). All of
these are optional: if anything is missing we log and return an empty string so
ingestion continues without crashing.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class OCRService:

    @staticmethod
    def available() -> bool:
        try:
            import pytesseract  # noqa: F401
            from PIL import Image  # noqa: F401
        except Exception:
            return False
        return True

    @staticmethod
    def extract(image_path: str) -> str:
        if not OCRService.available():
            logger.warning("OCR requested but pytesseract/Pillow unavailable.")
            return ""

        import pytesseract
        from PIL import Image

        try:
            return pytesseract.image_to_string(Image.open(image_path)).strip()
        except Exception:  # pragma: no cover - runtime/tesseract binary
            logger.exception("OCR failed for %s", image_path)
            return ""

    @staticmethod
    def extract_pdf(pdf_path: str) -> str:
        """OCR a scanned PDF, if pdf2image + tesseract are installed."""

        try:
            import pytesseract
            from pdf2image import convert_from_path
        except Exception:
            logger.warning("PDF OCR unavailable (need pdf2image + pytesseract).")
            return ""

        try:
            images = convert_from_path(pdf_path)
        except Exception:  # pragma: no cover - poppler missing
            logger.exception("pdf2image conversion failed for %s", pdf_path)
            return ""

        pages = []
        for index, image in enumerate(images, start=1):
            try:
                text = pytesseract.image_to_string(image).strip()
            except Exception:
                text = ""
            pages.append(f"<!-- page:{index} -->\n{text}")

        return "\n\n".join(pages).strip()
