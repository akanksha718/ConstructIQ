import os

from app.ingestion.parser import IndustrialParser

from app.ingestion.chunker import IndustrialChunker

from app.ingestion.matadata import MetadataExtractor

from app.ingestion.extractor import KnowledgeExtractor

from app.graph.graph_builder import GraphBuilder

from app.vectorstore.indexer import VectorIndexer
from app.intelligence.equipment_linker import EquipmentLinker
from app.models.document_chunk import DocumentChunk
from app.vectorstore.embedding_service import EmbeddingService
from app.services.storage_service import StorageService
from app.parsers.factory import ParserFactory
from app.graph.graph_service import KnowledgeGraphService


class IngestionPipeline:

    def __init__(self):

        self.parser = IndustrialParser()

        self.chunker = IndustrialChunker()

        self.metadata = MetadataExtractor()

        self.extractor = KnowledgeExtractor()

    async def run(

        self,

        document,

        db,

    ):

        local_file = await StorageService.download_file(

            document.storage_path

        )

        parser = ParserFactory.get_parser(document.filename)
        markdown = parser.parse(local_file)

        metadata = self.metadata.extract(

            local_file

        )
        all_extractions = []

        chunks = self.chunker.create_chunks(

            markdown

        )

        graph = GraphBuilder(db)

        stored_chunks = []

        for idx, chunk in enumerate(chunks):

            db_chunk = DocumentChunk(

                document_id=document.id,

                chunk_index=idx,

                page_number=chunk.metadata.get(

                    "page",

                    1,

                ),

                heading=chunk.metadata.get(

                    "heading",

                ),

                section=chunk.metadata.get(

                    "section",

                ),

                content=chunk.page_content,

            )

            db.add(db_chunk)

            db.flush()

            extraction = self.extractor.extract(

                chunk.page_content

            )

            all_extractions.append(extraction)

            graph.build(

                extraction,

                document,

                db_chunk,

            )

            stored_chunks.append(db_chunk)
        EmbeddingService.store_chunks(
            stored_chunks
        )
        KnowledgeGraphService.build(

            extraction,

            document.id,

        )
        os.remove(local_file)
        db.commit()

        