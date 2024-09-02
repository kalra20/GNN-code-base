from neo4j import GraphDatabase
import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.utils import from_networkx
import networkx as nx
from utils.configurations import config

NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD = config()

class GNN:

    def __init__(self, **kwargs):
        """
        Set some parameters
        """
        G = kwargs["graph"]

    def train_GNN():

        """
        pytorch training
        
        """
    
    def evaluate():
        """
        Offline evaluation
        
        """