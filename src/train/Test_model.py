import pytest
import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import SAGEConv


# The GraphSAGE model we want to test
class GraphSAGERecommender(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GraphSAGERecommender, self).__init__()
        self.sage1 = SAGEConv(in_channels, hidden_channels)
        self.sage2 = SAGEConv(hidden_channels, out_channels)
        self.link_predictor = torch.nn.Sequential(
            torch.nn.Linear(out_channels * 2, 1),  # Concatenate customer and merchant embeddings
            torch.nn.Sigmoid(),
        )

    def forward(self, data, pairs):
        x = self.sage1(data.x, data.edge_index)
        x = F.relu(x)
        x = self.sage2(x, data.edge_index)

        src_embeddings = x[pairs[:, 0]]
        dst_embeddings = x[pairs[:, 1]]

        edge_embeddings = torch.cat([src_embeddings, dst_embeddings], dim=1)
        link_probs = self.link_predictor(edge_embeddings).squeeze()

        return link_probs


# Define fixtures for pytest
@pytest.fixture
def graph_data():
    """Fixture for dummy graph data"""
    return Data(
        x=torch.rand(10, 3),  # 10 nodes, 3 features per node
        edge_index=torch.tensor([[0, 1, 2], [1, 2, 3]], dtype=torch.long),  # Simple edge index
    )


@pytest.fixture
def pairs():
    """Fixture for customer-merchant pairs"""
    return torch.tensor([[0, 4], [1, 5], [2, 6]], dtype=torch.long)


@pytest.fixture
def model():
    """Fixture for initializing the GraphSAGERecommender model"""
    return GraphSAGERecommender(in_channels=3, hidden_channels=4, out_channels=2)


@pytest.fixture
def labels():
    """Fixture for binary labels"""
    return torch.tensor([1, 0, 1], dtype=torch.float)


# Test class using pytest
def test_forward_pass(graph_data, pairs, model):
    """Test that the model's forward pass runs
    and produces the correct shape"""
    model.eval()
    with torch.no_grad():
        out = model(graph_data, pairs)
        assert out.shape[0] == pairs.shape[0], "Output shape does not match number of pairs"


def test_forward_pass_value(graph_data, pairs, model):
    """Ensure the model outputs probabilities between 0 and 1"""
    model.eval()
    with torch.no_grad():
        out = model(graph_data, pairs)
        assert torch.all(out >= 0) and torch.all(out <= 1), "Output is not in the range [0, 1]"


# To run with pytest, use:
# pytest -q test_recommender.py
