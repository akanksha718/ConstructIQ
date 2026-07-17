from app.graph.graph_builder import GraphBuilder


class KnowledgeGraphService:

    @staticmethod
    def build(

        extraction,

        document_id,

    ):

        graph = GraphBuilder()

        graph.add_document(document_id)

        for equipment in extraction.get(

            "equipment",

            [],

        ):

            graph.add_equipment(

                equipment

            )

            graph.connect_document(

                equipment,

                document_id,

            )