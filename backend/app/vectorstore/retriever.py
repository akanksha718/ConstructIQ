from app.vectorstore.pgvector import vector_store


class VectorRetriever:

    @staticmethod
    def retrieve(

        query,

        k=8,

    ):

        return vector_store.similarity_search(

            query,

            k=k,

        )