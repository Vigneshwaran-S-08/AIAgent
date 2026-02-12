import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

with open("data/repo_data.json", "r") as f:
    repo_data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
metadata = []

for commit in repo_data:
    for change in commit["changes"]:
        text = f"""
        Commit ID: {commit['commit_id']}
        Author: {commit['author']}
        Date: {commit['date']}
        Message: {commit['message']}
        File: {change['file_path']}
        Diff:
        {change['diff']}
        """

        documents.append(text)

        metadata.append({
            "commit_id": commit["commit_id"],
            "author": commit["author"],
            "date": commit["date"],
            "message": commit["message"],
            "file_path": change["file_path"],
            "diff": change["diff"]
        })

embeddings = model.encode(documents)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, "data/index.faiss")

with open("data/meta.json", "w") as f:
    json.dump(metadata, f)

print("Vector index with diffs created.")
