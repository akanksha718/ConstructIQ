from app.vectorstore.pgvector import vector_store


class VectorIndexer:

    @staticmethod
    def index(

        document_id,

        chunks,

    ):

        texts = []

        metadatas = []

        ids = []

        for chunk in chunks:

            texts.append(

                chunk.content

            )

            ids.append(

                str(chunk.id)

            )

            metadatas.append(

                {

                    "document_id": document_id,

                    "page": chunk.page_number,

                    "heading": chunk.heading,

                    "chunk_id": chunk.id,

                }

            )

        vector_store.add_texts(

            texts=texts,

            metadatas=metadatas,

            ids=ids,

        )