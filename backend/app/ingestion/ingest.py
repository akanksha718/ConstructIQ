from app.ingestion.parser import IndustrialParser

from app.ingestion.chunker import IndustrialChunker

from app.ingestion.extractor import KnowledgeExtractor

from app.vectorstore.indexer import VectorIndexer


class IngestionPipeline:

    def __init__(self):

        self.parser = IndustrialParser()

        self.chunker = IndustrialChunker()

        self.extractor = KnowledgeExtractor()

    def ingest(

        self,

        document,

        path,

        db

    ):

        parsed = self.parser.parse(path)

        chunks = self.chunker.create_chunks(parsed)

        extracted = []

        for chunk in chunks:

            extraction = self.extractor.extract(chunk)

            extracted.append(

                (

                    chunk,

                    extraction

                )

            )

        VectorIndexer.index(

            document.id,

            chunks

        )

        return extracted