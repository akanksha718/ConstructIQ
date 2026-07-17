from app.vectorstore.retriever import VectorRetriever


class SearchService:

    @staticmethod
    def search(

        query,

        k=8,

    ):

        return VectorRetriever.retrieve(

            query,

            k,

        )