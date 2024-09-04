from neo4j import GraphDatabase
from utils.configurations import config
import torch

class GenerateLabels:
    def __init__(self) -> None:
        
        NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD = config()

        # Connect to Neo4j
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
    def training_data(self):

        # Fetch the data
        with self.driver.session() as session:
            samples = session.read_transaction(self.fetch_samples)
        
        self.driver.close()
        
        # Convert to PyTorch tensors
        customer_ids = torch.tensor([sample[0] for sample in samples], dtype=torch.long)
        merchant_ids = torch.tensor([sample[1] for sample in samples], dtype=torch.long)
        labels = torch.tensor([sample[2] for sample in samples], dtype=torch.float)

        # Combine customer and merchant IDs into pairs
        pairs = torch.stack((customer_ids, merchant_ids), dim=1)

        return pairs, labels

    def fetch_samples(self, tx):
        # Cypher query to get the samples and labels
        # TODO: Add jinja template later
        cypher_query = """ MATCH (c:Customer)-[r:ORDERS|VISITS]->(m:Merchant)
                WITH id(c) AS customer_id, id(m) AS merchant_id, 1 AS label
                RETURN 
                UNION
                MATCH (c:Customer), (m:Merchant)
                WHERE NOT EXISTS {
                    MATCH (c)-[:ORDERS|VISITS]->(m)
                }
                WITH id(c) AS customer_id, id(m) AS merchant_id, 0 AS label
                LIMIT 100
                RETURN customer_id, merchant_id, label """

        result = tx.run(cypher_query)
        return [(record["customer_id"], record["merchant_id"], record["label"]) for record in result]
