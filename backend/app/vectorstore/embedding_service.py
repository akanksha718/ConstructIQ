from app.vectorstore.pgvector import vector_store


class EmbeddingService:

    @staticmethod
    def store_chunks(chunks):

        texts = []

        metadatas = []

        ids = []

        for chunk in chunks:

            texts.append(chunk.content)

            ids.append(str(chunk.id))

            metadatas.append(

                {
                    "document_id": chunk.document_id,
                    "page": chunk.page_number,
                    "heading": chunk.heading,
                    "section": chunk.section,
                    "chunk_id": chunk.id,
                }

            )

        vector_store.add_texts(

            texts=texts,

            metadatas=metadatas,

            ids=ids,

        )