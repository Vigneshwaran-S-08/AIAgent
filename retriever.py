import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load indexed repo data
with open("data/repo_data.json", "r") as f:
    repo_data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
metadata = []

for entry in repo_data:
    for change in entry["changes"]:
        text = f"""
        Commit ID: {entry['commit_id']}
        Author: {entry['author']}
        Date: {entry['date']}
        Message: {entry['message']}
        File: {change['file_path']}
        Content:
        {change['content']}
        """

        documents.append(text)

        metadata.append({
            "commit_id": entry["commit_id"],
            "author": entry["author"],
            "date": entry["date"],
            "message": entry["message"],
            "file_path": change["file_path"],
            "content": change["content"]
        })

# Generate embeddings
embeddings = model.encode(documents)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

# Save index
faiss.write_index(index, "data/index.faiss")

# Save metadata
with open("data/meta.json", "w") as f:
    json.dump(metadata, f)

print("Vector index created successfully (including file contents).")
