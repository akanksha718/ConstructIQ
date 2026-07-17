"""Selects a parser for a document based on its file extension.

Every parser exposes ``parse(file_path) -> str`` returning plain text / markdown.
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.parsers.pdf_parser import PDFParser
from app.parsers.excel_parser import ExcelParser
from app.parsers.email_parser import EmailParser
from app.parsers.pid_parser import PIDParser
from app.parsers.ocr import OCRService

logger = logging.getLogger(__name__)


class TextParser:
    def parse(self, file_path: str) -> str:
        try:
            with open(file_path, encoding="utf-8", errors="ignore") as fh:
                return fh.read()
        except Exception:
            logger.exception("Failed to read text file %s", file_path)
            return ""


class ImageParser:
    def parse(self, file_path: str) -> str:
        return OCRService.extract(file_path)


class ParserFactory:

    @staticmethod
    def get_parser(filename: str):
        ext = Path(filename).suffix.lower()

        if ext == ".pdf":
            return PDFParser()

        if ext in {".xlsx", ".xls", ".csv"}:
            return ExcelParser()

        if ext in {".msg", ".eml"}:
            return EmailParser()

        if ext in {".dwg", ".dxf"}:
            return PIDParser()

        if ext in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            return ImageParser()

        if ext in {".txt", ".md"}:
            return TextParser()

        # Unknown -> best-effort plain text read.
        return TextParser()

    @staticmethod
    def parse(filename: str, file_path: str) -> str:
        return ParserFactory.get_parser(filename).parse(file_path)
