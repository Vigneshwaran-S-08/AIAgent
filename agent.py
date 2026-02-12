import faiss
import json
import numpy as np
import sys
from sentence_transformers import SentenceTransformer

if len(sys.argv) < 2:
    print("Usage: python agent.py \"your question\"")
    sys.exit(1)

question = sys.argv[1]

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("data/index.faiss")

# Load metadata
with open("data/meta.json", "r") as f:
    metadata = json.load(f)

# Embed question
query_vector = model.encode([question])
query_vector = np.array(query_vector).astype("float32")

# Search
D, I = index.search(query_vector, k=3)

print("\nTop Relevant Commits:\n")

for idx in I[0]:
    commit = metadata[idx]
    print("--------------------------------------------------")
    print("Commit ID:", commit["commit_id"])
    print("Author:", commit["author"])
    print("Date:", commit["date"])
    print("Message:", commit["message"])
    print("--------------------------------------------------\n")
