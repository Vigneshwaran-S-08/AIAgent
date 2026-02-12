from git import Repo

repo = Repo(".")

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


def get_file_history(file_name):
    commits = list(repo.iter_commits(paths=file_name))
    history = []

    for commit in commits:
        history.append({
            "commit_id": commit.hexsha,
            "author": commit.author.name,
            "date": str(commit.committed_datetime),
            "message": commit.message.strip()
        })

    return history


def get_latest_file_content(file_name):
    try:
        blob = repo.head.commit.tree / file_name
        return blob.data_stream.read().decode("utf-8", errors="ignore")
    except Exception:
        return None


def get_file_diff(commit_id):
    commit = repo.commit(commit_id)
    diffs = []

    for parent in commit.parents:
        for diff in parent.diff(commit, create_patch=True):
            try:
                diff_text = diff.diff.decode("utf-8", errors="ignore")
            except:
                diff_text = ""

            file_path = diff.a_path if diff.a_path else diff.b_path

            diffs.append({
                "file": file_path,
                "diff": diff_text
            })

    return diffs
