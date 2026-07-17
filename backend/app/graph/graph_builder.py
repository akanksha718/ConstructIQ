from app.graph.neo4j_client import Neo4jClient


class GraphBuilder:

    def __init__(self):

        self.client = Neo4jClient()

    def add_equipment(self, tag):

        self.client.execute(
            """
            MERGE (e:Equipment {tag:$tag})
            """,
            tag=tag,
        )

    def add_document(self, document_id):

        self.client.execute(
            """
            MERGE (d:Document {id:$id})
            """,
            id=document_id,
        )

    def connect_document(

        self,

        tag,

        document_id,

    ):

        self.client.execute(
            """
            MATCH (e:Equipment {tag:$tag})
            MATCH (d:Document {id:$id})

            MERGE (d)-[:MENTIONS]->(e)
            """,
            tag=tag,
            id=document_id,
        )