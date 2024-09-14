# from neo4j import GraphDatabase
# import pandas as pd
import torch

# from torch_geometric.data import Data
from torch_geometric.utils import from_networkx
import networkx as nx

# from utils.configurations import config
from GraphSage import GraphSAGE
from Load_data.generate_labels import GenerateLabels


class GNN:
    def __init__(self, **kwargs: dict):
        """
        Set some parameters
        """
        self.G = nx.Graph()
        self.nodes_df = kwargs["nodes"]
        self.relationships_df = kwargs["relationships"]

    def prepare_graph(self):
        # Add nodes with attributes
        for _, row in self.nodes_df.iterrows():
            node_id = row["id"]
            node_type = row["labels"][0]  # Assuming a single label per node
            node_features = row["properties"]

            self.G.add_node(node_id, label=node_type, **node_features)

        # Add edges with attributes
        for _, row in self.relationships_df.iterrows():
            source = row["source"]
            target = row["target"]
            edge_type = row["type"]

            self.G.add_edge(source, target, label=edge_type)

        print(
            f"Graph has {self.G.number_of_nodes()} nodes \
            and {self.G.number_of_edges()} edges."
        )

    def networkx_to_pyg(self):
        # Convert NetworkX graph to PyTorch Geometric Data object
        graph = from_networkx(self.G)
        return graph

    def training_prepare(self, graph):
        """
        pytorch training

        """
        # Initialize the model
        self.model = GraphSAGE(in_channels=graph.x.shape[1], hidden_channels=64, out_channels=128)

        # Define optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01, weight_decay=5e-4)
        self.criterion = torch.nn.BCELoss()

        label_generator = GenerateLabels()
        pairs, labels = label_generator.training_data()

        return pairs, labels

    def train_GNN(self, graph, pairs, labels, epochs: int = 2):
        self.model.train()  # Set the model to training mode

        for epoch in range(epochs):
            self.optimizer.zero_grad()  # Zero out gradients

            # Forward pass: get predictions
            link_probs = self.model(graph, pairs)

            # Calculate loss
            loss = self.criterion(link_probs, labels)

            # Backward pass: compute gradients and update weights
            loss.backward()
            self.optimizer.step()

            if epoch != 0:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    def evaluate(self, graph, pairs, labels):
        self.model.eval()  # Set the model to evaluation mode

        with torch.no_grad():  # Disable gradient computation
            link_probs = self.model(graph, pairs)
            predictions = (link_probs > 0.5).float()  # Classify as 1 if probability > 0.5

            accuracy = (predictions == labels).sum().item() / labels.size(0)
            # return accuracy

        print(f"Accuracy: {accuracy:.4f}")
