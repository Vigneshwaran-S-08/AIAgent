import faiss
import json
import numpy as np
import sys
from sentence_transformers import SentenceTransformer

if len(sys.argv) < 2:
    print("Usage: python agent.py \"your question\"")
    sys.exit(1)

question = sys.argv[1].lower()

# Load metadata
with open("data/meta.json", "r") as f:
    metadata = json.load(f)

# ------------------------------
# 1️⃣ Check if question mentions a file directly
# ------------------------------
for entry in metadata:
    if entry["commit_id"] == "LATEST_VERSION":
        file_name = entry["file_path"].split("/")[-1].lower()

        if file_name in question:
            print("\nLatest Version Found:\n")
            print("File:", entry["file_path"])
            print("\nFull Content:\n")
            print(entry["content"])
            sys.exit(0)

# ------------------------------
# 2️⃣ Otherwise use semantic search
# ------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("data/index.faiss")

query_vector = model.encode([question])
query_vector = np.array(query_vector).astype("float32")

D, I = index.search(query_vector, k=3)

print("\nTop Relevant Results:\n")

for idx in I[0]:
    result = metadata[idx]
    print("--------------------------------------------------")
    print("Commit ID:", result["commit_id"])
    print("Author:", result["author"])
    print("Date:", result["date"])
    print("File:", result["file_path"])
    print("Message:", result["message"])
    print("\nContent Preview:\n")
    print(result["content"][:800])
    print("--------------------------------------------------\n")
