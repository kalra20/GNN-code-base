
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class GraphSAGERecommender(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GraphSAGERecommender, self).__init__()
        self.sage1 = SAGEConv(in_channels, hidden_channels)
        self.sage2 = SAGEConv(hidden_channels, out_channels)
        self.link_predictor = nn.Sequential(
            nn.Linear(out_channels * 2, 1),  # Concatenate customer and merchant embeddings
            nn.Sigmoid()
        )

    def forward(self, data, pairs):
        # Step 1: Generate node embeddings using GraphSAGE
        x = self.sage1(data.x, data.edge_index)
        x = F.relu(x)
        x = self.sage2(x, data.edge_index)
        
        # Step 2: Prepare embeddings for customer-merchant pairs
        src_embeddings = x[pairs[:, 0]]  # Embeddings for customers
        dst_embeddings = x[pairs[:, 1]]  # Embeddings for merchants
        
        # Step 3: Concatenate and predict link existence
        edge_embeddings = torch.cat([src_embeddings, dst_embeddings], dim=1)
        link_probs = self.link_predictor(edge_embeddings).squeeze()
        
        return link_probs