import os
import json
from git import Repo

repo = Repo(".")

data = []

# -------------------------
# 1. Extract Commit History
# -------------------------
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

            # 🔥 FIX: Handle new file correctly
            file_path = diff.a_path if diff.a_path else diff.b_path

            change = {
                "file_path": file_path,
                "content": diff_text
            }

            commit_data["changes"].append(change)

    data.append(commit_data)

# ---------------------------------
# 2. Add Latest File Contents (NEW)
# ---------------------------------
for blob in repo.tree().traverse():
    if blob.type == "blob":
        try:
            content = blob.data_stream.read().decode("utf-8", errors="ignore")
        except:
            content = ""

        file_entry = {
            "commit_id": "LATEST_VERSION",
            "author": "N/A",
            "date": "N/A",
            "message": "Latest file snapshot",
            "changes": [
                {
                    "file_path": blob.path,
                    "content": content
                }
            ]
        }

        data.append(file_entry)

# Save everything
os.makedirs("data", exist_ok=True)

with open("data/repo_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Repository indexed successfully with commits + latest file content.")
