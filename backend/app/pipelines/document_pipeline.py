class DocumentPipeline:

    async def run(self, document_id: int):

        """
        1 Download

        2 Parse

        3 OCR if needed

        4 Chunk

        5 Metadata

        6 Entity Extraction

        7 Graph

        8 Embeddings

        9 Finish
        """