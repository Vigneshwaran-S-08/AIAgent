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
        "changes": []
    }

    for parent in commit.parents:
        diffs = parent.diff(commit, create_patch=True)

        for diff in diffs:
            try:
                diff_text = diff.diff.decode("utf-8", errors="ignore")
            except:
                diff_text = ""

            change = {
                "file_path": diff.a_path,
                "diff": diff_text
            }

            commit_data["changes"].append(change)

    data.append(commit_data)

os.makedirs("data", exist_ok=True)

with open("data/repo_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Repository indexed with diffs successfully.")
