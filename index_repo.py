import os
import json
from git import Repo

repo = Repo(".")

data = []

for commit in repo.iter_commits():
    commit_data = {
        "commit_id": commit.hexsha,
        "author": commit.author.name,
        "date": str(commit.committed_datetime),
        "message": commit.message,
        "files": []
    }

    for parent in commit.parents:
        diffs = parent.diff(commit, create_patch=True)
        for diff in diffs:
            file_change = {
                "file_path": diff.a_path,
                "diff": diff.diff.decode("utf-8", errors="ignore")
            }
            commit_data["files"].append(file_change)

    data.append(commit_data)

os.makedirs("data", exist_ok=True)

with open("data/repo_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Repository indexed successfully.")

