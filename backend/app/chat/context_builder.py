class ContextBuilder:

    @staticmethod
    def build(

        graph_results,

        vector_results

    ):

        context = []

        for item in graph_results:

            context.append(item)

        for doc in vector_results:

            context.append(

                doc.page_content

            )

        return "\n\n".join(context)