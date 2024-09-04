# GNN-code-base

GNN Customer Recommendation System using GraphSAGE
Project Overview
This project implements a Graph Neural Network (GNN) model using the GraphSAGE algorithm to generate personalized recommendations for customers. The model learns customer embeddings by leveraging graph-based relationships such as customer interactions, product purchases, and social connections. These embeddings are then used to recommend relevant products to customers.

Key Features
GraphSAGE: A state-of-the-art algorithm for generating embeddings for large-scale, dynamic graphs.
Customer Recommendations: Recommend products based on learned embeddings.
Scalable Approach: Handles large graphs efficiently with the inductive learning approach of GraphSAGE.
Modular Design: Allows easy customization and integration with other data sources or models.
Table of Contents
Installation
Usage
Model Overview
Data Preparation
Training the Model
Generating Recommendations
Pre-commit Hooks
Contributing
License
Installation
Follow these steps to set up the project locally:

Clone this repository:

```
git clone https://github.com/kalra20/GNN-code-base.git
cd GNN-code-base
Create and activate a virtual environment (optional but recommended):
```

```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required dependencies:
```

```
pip install -r requirements.txt
Install the pre-commit hooks (optional but recommended):
```

```
pre-commit install
```

Usage

1. Model Overview
   The GraphSAGE algorithm is designed to learn useful node embeddings by sampling and aggregating features from neighboring nodes. This approach is highly efficient for large, evolving graphs where it is computationally expensive to retrain the entire model. We apply this to the customer-product interaction graph to generate embeddings that are later used for recommendations.

2. Data Preparation
   The input data should represent a graph structure where nodes represent customers and products, and edges represent interactions between customers and merchants (e.g., purchases, views). The graph can also include additional features such as customer demographics and merchant details.

Sample format for edge data (CSV):

```
customer_id,product_id,interaction_type
123,456,purchase
124,789,view
...
```

Ensure that your dataset is prepared in the correct format before proceeding to training.

3. Training the Model
   To train the GraphSAGE model:

Preprocess the graph data (customer-merchant interactions) using the provided script:

Train the GraphSAGE model:

4. Generating Recommendations
   Once the model is trained, you can generate product recommendations for a specific customer by running:

```
python recommend.py --customer_id 123 --top_k 10
```

This will output the top 10 recommended products for the customer with ID 123.

5. Pre-commit Hooks
   The project includes several pre-commit hooks to ensure code quality and consistency. These hooks run automatically on every commit and include:

Trailing whitespace remover
End-of-file fixer
YAML file syntax checker
Python linters (flake8, black, isort)
To run the pre-commit hooks manually, execute:

```
pre-commit run --all-files
```

The configuration for the pre-commit hooks is available in the .pre-commit-config.yaml file.
