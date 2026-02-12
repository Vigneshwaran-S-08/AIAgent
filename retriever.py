import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load repo data
with open("data/repo_data.json", "r") as f:
    repo_data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
metadata = []

for commit in repo_data:
    text = f"""
    Commit ID: {commit['commit_id']}
    Author: {commit['author']}
    Date: {commit['date']}
    Message: {commit['message']}
    """
    documents.append(text)
    metadata.append(commit)

# Create embeddings locally
embeddings = model.encode(documents)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save index
faiss.write_index(index, "data/index.faiss")

# Save metadata
with open("data/meta.json", "w") as f:
    json.dump(metadata, f)

print("Offline vector index created successfully.")
