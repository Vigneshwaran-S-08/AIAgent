import faiss
import json
import numpy as np
import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

question = sys.argv[1]

# Load index
index = faiss.read_index("data/index.faiss")

with open("data/meta.json", "r") as f:
    metadata = json.load(f)

# Embed question
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=question
)

query_vector = np.array([response.data[0].embedding]).astype("float32")

# Search
D, I = index.search(query_vector, k=3)

context = ""
for idx in I[0]:
    commit = metadata[idx]
    context += f"""
    Commit ID: {commit['commit_id']}
    Author: {commit['author']}
    Date: {commit['date']}
    Message: {commit['message']}
    """

# Ask LLM
chat_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a Git repository analysis agent."},
        {"role": "user", "content": f"""
        Context:
        {context}

        Question:
        {question}

        Answer clearly mentioning commit ID, author, and description.
        """}
    ]
)

print(chat_response.choices[0].message.content)

