from app.vectorstore.pgvector import vector_store


class VectorSearcher:

    @staticmethod
    def search(

        question: str,

        k: int = 10,

    ):

        return vector_store.similarity_search(

            question,

            k=k,

        )