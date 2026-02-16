import sys
import re
from git_utils import (
    get_latest_commits,
    get_file_history,
    get_latest_file_content,
    get_file_diff
)
from llm_utils import ask_llm


if len(sys.argv) < 2:
    print("Usage: python agent.py \"your question\"")
    sys.exit(1)

question = sys.argv[1].lower()


# -------------------------
# Extract file name
# -------------------------
def extract_file_name(text):
    match = re.search(r'\b[\w\-]+\.c\b|\b[\w\-]+\.py\b|\b[\w\-]+\.md\b', text)
    return match.group(0) if match else None


file_name = extract_file_name(question)


# -------------------------
# 1️⃣ Latest commits
# -------------------------
if "latest commit" in question or "recent commit" in question:
    commits = get_latest_commits(5)

    print("\nLatest 5 Commits:\n")
    for c in commits:
        print("--------------------------------------------------")
        print("Commit ID:", c["commit_id"])
        print("Author:", c["author"])
        print("Date:", c["date"])
        print("Message:", c["message"])
    print("--------------------------------------------------")
    sys.exit(0)


# -------------------------
# 2️⃣ Who modified file
# -------------------------
if "who modified" in question and file_name:
    history = get_file_history(file_name)

    if not history:
        print(f"No history found for {file_name}")
        sys.exit(0)

    print(f"\nModification History for {file_name}:\n")

    for h in history:
        print("--------------------------------------------------")
        print("Commit ID:", h["commit_id"])
        print("Author:", h["author"])
        print("Date:", h["date"])
        print("Message:", h["message"])
    print("--------------------------------------------------")
    sys.exit(0)


# -------------------------
# 3️⃣ What changed in file
# -------------------------
if "what changed" in question and file_name:
    history = get_file_history(file_name)

    if not history:
        print(f"No history found for {file_name}")
        sys.exit(0)

    latest_commit = history[0]["commit_id"]
    diffs = get_file_diff(latest_commit, file_name)

    print(f"\nLatest Changes in {file_name}:\n")

    if not diffs:
        print("No changes found.")
    else:
        for diff in diffs:
            print(diff)

    sys.exit(0)


# -------------------------
# 4️⃣ Explain file logic
# -------------------------
if ("what does" in question or "explain" in question) and file_name:
    content = get_latest_file_content(file_name)

    if not content:
        print(f"File not found: {file_name}")
        sys.exit(0)

    prompt = f"""
You are a senior software engineer.

Analyze this code and explain:
1. What it does
2. Logical mistakes
3. Improvements needed

Code:
{content}
"""

    answer = ask_llm(prompt)
    print("\nAI Analysis:\n")
    print(answer)
    sys.exit(0)


# -------------------------
# 5️⃣ Fallback → LLM
# -------------------------
answer = ask_llm(question)
print("\nAI Response:\n")
print(answer)
