from neo4j import GraphDatabase
import os


class Neo4jClient:

    def __init__(self):

        self.driver = GraphDatabase.driver(

            os.getenv("NEO4J_URI"),

            auth=(

                os.getenv("NEO4J_USER"),

                os.getenv("NEO4J_PASSWORD"),

            ),

        )

    def execute(self, query, **params):

        with self.driver.session() as session:

            session.run(query, params)