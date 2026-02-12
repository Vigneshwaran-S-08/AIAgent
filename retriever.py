import json
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

with open("data/repo_data.json", "r") as f:
    repo_data = json.load(f)

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

embeddings = []

for doc in documents:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )
    embeddings.append(response.data[0].embedding)

dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype("float32"))

faiss.write_index(index, "data/index.faiss")

with open("data/meta.json", "w") as f:
    json.dump(metadata, f)

print("Vector index created.")

