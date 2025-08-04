# predict_model.py: Insomnia prediction using GNN, XGBoost, and ensemble models
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
import torch_geometric
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define GNN model architecture
class GCN(torch.nn.Module):
    def __init__(self):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(16, 32)
        self.conv2 = GCNConv(32, 2)
    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

# Set base path
BASE = Path('/content/intern_submissions/Alagappan_Alagappan')

# Load models with error handling
try:
    xgboost_model = joblib.load(BASE / 'xgboost_model.joblib')
    gnn_state_dict = joblib.load(BASE / 'gnn_model.joblib')
    ensemble_model = joblib.load(BASE / 'ensemble_model.joblib')
except FileNotFoundError as e:
    logging.error(f"Model file not found: {e}")
    exit(1)

# Initialize GNN model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
gnn_model = GCN().to(device)
gnn_model.load_state_dict(gnn_state_dict)
gnn_model.eval()

# Load test data
try:
    test_data = pd.read_csv(BASE / 'test_data.csv')
    gnn_test_data = torch.load(BASE / 'test_graph.pt')
except FileNotFoundError as e:
    logging.error(f"Test data file not found: {e}")
    exit(1)

# Sample inputs (use first test data point)
xgboost_sample = test_data[['num_adrs_scaled']].iloc[[0]].values
gnn_sample_x = gnn_test_data.x[:1]  # First drug node’s PCA features
gnn_sample_edge = torch.tensor([[0, 1], [1, 0]], dtype=torch.long).to(device)  # Mock edge
with torch.no_grad():
    gnn_embeddings = gnn_model.conv1(gnn_test_data.x, gnn_test_data.edge_index).relu().cpu().numpy()
ensemble_sample = np.hstack((gnn_embeddings[:1], xgboost_sample))

# XGBoost prediction
xgb_pred = xgboost_model.predict_proba(xgboost_sample)[:, 1][0]
xgb_label = 'High' if xgb_pred > 0.66 else 'Moderate' if xgb_pred > 0.33 else 'Low'
logging.info(f"XGBoost Sample Prediction: {{'probability': {xgb_pred:.4f}, 'label': '{xgb_label}'}}")

# GNN prediction
with torch.no_grad():
    gnn_data = Data(x=gnn_sample_x, edge_index=gnn_sample_edge).to(device)
    gnn_output = gnn_model(gnn_data)
    gnn_prob = torch.softmax(gnn_output, dim=1)[0, 1].item()
    gnn_label = 'High' if gnn_prob > 0.66 else 'Moderate' if gnn_prob > 0.33 else 'Low'
logging.info(f"GNN Sample Prediction: {{'probability': {gnn_prob:.4f}, 'label': '{gnn_label}'}}")

# Ensemble prediction
ensemble_pred = ensemble_model.predict_proba(ensemble_sample)[:, 1][0]
ensemble_label = 'High' if ensemble_pred > 0.66 else 'Moderate' if ensemble_pred > 0.33 else 'Low'
logging.info(f"Ensemble Sample Prediction: {{'probability': {ensemble_pred:.4f}, 'label': '{ensemble_label}'}}")

# Test set evaluation
X_test_xgb = test_data[['num_adrs_scaled']].values
y_test = test_data['target_flag'].values
X_test_ens = np.hstack((gnn_embeddings[:len(test_data)], X_test_xgb))

# XGBoost test
xgb_preds = xgboost_model.predict_proba(X_test_xgb)[:, 1]
xgb_labels = (xgb_preds > 0.5).astype(int)
print("\nXGBoost Test Results:")
print(classification_report(y_test, xgb_labels))
print(f"Accuracy: {accuracy_score(y_test, xgb_labels):.4f}")
print(f"ROC AUC: {roc_auc_score(y_test, xgb_preds):.4f}")

# GNN test
with torch.no_grad():
    drug_node_mask = torch.zeros(gnn_test_data.num_nodes, dtype=torch.bool)
    drug_node_mask[:len(test_data)] = True
    drug_subgraph_edge_index, _ = torch_geometric.utils.subgraph(drug_node_mask, gnn_test_data.edge_index.t(), relabel_nodes=True)
    gnn_out = gnn_model(Data(x=gnn_test_data.x[:len(test_data)], edge_index=drug_subgraph_edge_index).to(device))
    gnn_probs = torch.softmax(gnn_out, dim=1)[:, 1].cpu().numpy()
gnn_labels = (gnn_probs > 0.5).astype(int)
print("\nGNN Test Results:")
print(classification_report(y_test, gnn_labels))
print(f"Accuracy: {accuracy_score(y_test, gnn_labels):.4f}")
print(f"ROC AUC: {roc_auc_score(y_test, gnn_probs):.4f}")

# Ensemble test
ensemble_preds = ensemble_model.predict_proba(X_test_ens)[:, 1]
ensemble_labels = (ensemble_preds > 0.5).astype(int)
print("\nEnsemble Test Results:")
print(classification_report(y_test, ensemble_labels))
print(f"Accuracy: {accuracy_score(y_test, ensemble_labels):.4f}")
print(f"ROC AUC: {roc_auc_score(y_test, ensemble_preds):.4f}")

# t-SNE visualization
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(gnn_embeddings[:len(test_data)])
plt.figure(figsize=(8, 6))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c=test_data['target_flag'], cmap='coolwarm', alpha=0.6)
plt.title("t-SNE Visualization of GNN Embeddings (Test Set)")
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.colorbar(label="Insomnia (0: No, 1: Yes)")
plt.savefig(BASE / 'gnn_tsne.png')
plt.close()
logging.info("t-SNE plot saved to gnn_tsne.png")