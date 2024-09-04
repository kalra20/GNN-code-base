import pytest
import torch
from neo4j import GraphDatabase
from torch_geometric.data import Data
from Train.GraphSage import GraphSAGERecommender  # Assuming your model is in a file called my_model.py

# Neo4j fixture
@pytest.fixture(scope="module")
def neo4j_session():
    """Fixture for connecting to the Neo4j database."""
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "your_password"
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        yield session  # Provides a session object for Neo4j
    driver.close()

# Data Loading Test
def test_data_loading(neo4j_session):
    """Test the data loading process from Neo4j."""
    # Define your query here to extract customer-merchant pairs from Neo4j
    query = """
    MATCH (c:Customer)-[r:ORDERS|VISITS]->(m:Merchant)
    RETURN id(c) AS customer_id, id(m) AS merchant_id
    """
    
    def fetch_pairs(tx):
        result = tx.run(query)
        return [(record["customer_id"], record["merchant_id"]) for record in result]
    
    pairs = neo4j_session.read_transaction(fetch_pairs)
    
    # Check that data is being returned correctly
    assert len(pairs) > 0, "No customer-merchant pairs were loaded from the database."

    # Ensure pairs are in correct format
    assert isinstance(pairs[0], tuple), "Data should be returned as a list of tuples."