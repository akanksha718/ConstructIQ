from pathlib import Path

from app.parsers.pdf_parser import PDFParser
from app.parsers.excel_parser import ExcelParser
from app.parsers.email_parser import EmailParser
from app.parsers.pid_parser import PIDParser


class ParserFactory:

    @staticmethod
    def get_parser(filename: str):

        ext = Path(filename).suffix.lower()

        if ext == ".pdf":
            return PDFParser()

        if ext in [".xlsx", ".xls", ".csv"]:
            return ExcelParser()

        if ext in [".msg", ".eml"]:
            return EmailParser()

        if ext in [".dwg", ".dxf"]:
            return PIDParser()

        return PDFParser()