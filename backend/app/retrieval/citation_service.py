class CitationService:

    @staticmethod
    def build(results):

        citations = []

        for result in results:

            if hasattr(result, "metadata"):

                citations.append(

                    {

                        "document": result.metadata.get(

                            "document"

                        ),

                        "page": result.metadata.get(

                            "page"

                        ),

                        "heading": result.metadata.get(

                            "heading"

                        ),

                    }

                )

        return citations