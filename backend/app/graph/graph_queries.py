from neo4j import GraphDatabase
import os


driver = GraphDatabase.driver(

    os.getenv("NEO4J_URI"),

    auth=(

        os.getenv("NEO4J_USER"),

        os.getenv("NEO4J_PASSWORD"),

    ),

)


class GraphQueries:

    @staticmethod
    def equipment_documents(tag):

        with driver.session() as session:

            result = session.run(
                """
                MATCH (d)-[:MENTIONS]->(e:Equipment {tag:$tag})

                RETURN d.id
                """,
                tag=tag,
            )

            return [

                r["d.id"]

                for r in result

            ]