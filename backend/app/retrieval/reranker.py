class ResultReranker:

    @staticmethod
    def rerank(

        graph,

        vectors,

        metadata,

    ):

        merged = []

        merged.extend(graph)

        merged.extend(vectors)

        merged.extend(metadata)

        return merged