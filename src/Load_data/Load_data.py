from neo4j import GraphDatabase
import pandas as pd
from utils.configurations import config

class LoadGraph:

    def __init__(self):
        """
        Set some parameters
        """
        NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD = config()
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        # G = kwargs["graph"]

    def get_nodes(self, tx):
        query = "MATCH (n) RETURN id(n) AS id, labels(n) AS labels, properties(n) AS properties"
        result = tx.run(query)
        return [record.data() for record in result]
    
    def get_relationships(self, tx):
        query = """
        MATCH (a)-[r]->(b)
        RETURN id(a) AS source, id(b) AS target, type(r) AS type, properties(r) AS properties
        """
        result = tx.run(query)
        return [record.data() for record in result]
    
    def get_nodes_realtionships(self):
    
        with self.driver.session() as session:
            nodes = session.read_transaction(self.get_nodes)
            relationships = session.read_transaction(self.get_relationships)

        self.driver.close()

        # Convert to DataFrames for easier manipulation
        nodes_df = pd.DataFrame(nodes)
        relationships_df = pd.DataFrame(relationships)

        return nodes_df, relationships_df
        # print("Nodes:")
        # print(nodes_df.head())

        # print("\nRelationships:")
        # print(relationships_df.head())