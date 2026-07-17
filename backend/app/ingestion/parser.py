from pathlib import Path

from docling.document_converter import DocumentConverter


class IndustrialParser:

    def __init__(self):

        self.converter = DocumentConverter()

    def parse(self, file_path: str):

        """
        Parse industrial document using Docling.

        Returns markdown preserving
        headings, tables and layout.
        """

        result = self.converter.convert(file_path)

        document = result.document

        return document.export_to_markdown()