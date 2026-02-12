from git import Repo

repo = Repo(".")

# ---------------------------
# Resolve filename automatically
# ---------------------------
def resolve_file_path(file_name):
    for blob in repo.head.commit.tree.traverse():
        if blob.type == "blob":
            if blob.path.endswith(file_name):
                return blob.path
    return None


# ---------------------------
# Latest commits
# ---------------------------
def get_latest_commits(n=5):
    commits = list(repo.iter_commits())[:n]
    results = []

    for commit in commits:
        results.append({
            "commit_id": commit.hexsha,
            "author": commit.author.name,
            "date": str(commit.committed_datetime),
            "message": commit.message.strip()
        })

    return results


# ---------------------------
# File history
# ---------------------------
def get_file_history(file_name):
    full_path = resolve_file_path(file_name)

    if not full_path:
        return []

    commits = list(repo.iter_commits(paths=full_path))
    history = []

    for commit in commits:
        history.append({
            "commit_id": commit.hexsha,
            "author": commit.author.name,
            "date": str(commit.committed_datetime),
            "message": commit.message.strip()
        })

    return history


# ---------------------------
# Latest file content
# ---------------------------
def get_latest_file_content(file_name):
    full_path = resolve_file_path(file_name)

    if not full_path:
        return None

    try:
        blob = repo.head.commit.tree / full_path
        return blob.data_stream.read().decode("utf-8", errors="ignore")
    except:
        return None


# ---------------------------
# File diff for specific commit
# ---------------------------
def get_file_diff(commit_id, file_name):
    full_path = resolve_file_path(file_name)

    if not full_path:
        return []

    commit = repo.commit(commit_id)
    diffs = []

    for parent in commit.parents:
        for diff in parent.diff(commit, create_patch=True):
            file_path = diff.a_path if diff.a_path else diff.b_path

            if file_path == full_path:
                try:
                    diff_text = diff.diff.decode("utf-8", errors="ignore")
                except:
                    diff_text = ""

                diffs.append(diff_text)

    return diffs
