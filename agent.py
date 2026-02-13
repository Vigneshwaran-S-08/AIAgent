import subprocess
import os
import re

# 🔧 Set your repository path here
REPO_PATH = "/absolute/path/to/your/repo"   # <-- CHANGE THIS


# =========================
# 🔹 LLM FUNCTION (Concise)
# =========================
def ask_llm(user_prompt):
    strict_prompt = f"""
You are a professional Git and code assistant.

Rules:
- Be concise and precise.
- Maximum 5-6 sentences.
- No unnecessary explanation.
- Use bullet points if helpful.
- Be technical and clean.

Task:
{user_prompt}
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],   # change model if needed
        input=strict_prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()


# =========================
# 🔹 GIT FUNCTIONS
# =========================

def who_modified_file(filename):
    result = subprocess.run(
        ["git", "log", "--pretty=format:%h - %an - %s", "--", filename],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    )

    if not result.stdout.strip():
        return f"No commits found for {filename}"

    return result.stdout.strip()


def latest_commits(n=5):
    result = subprocess.run(
        ["git", "log", f"-n{n}", "--pretty=format:%h - %an - %s"],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    )

    return result.stdout.strip()


def summarize_recent_commits(n=5):
    result = subprocess.run(
        ["git", "log", f"-n{n}", "--pretty=format:%h - %s"],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    )

    commits = result.stdout.strip()

    prompt = f"""
Summarize the following recent commits briefly:

{commits}
"""
    return ask_llm(prompt)


def explain_last_commit_diff():
    result = subprocess.run(
        ["git", "show"],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    )

    diff = result.stdout

    prompt = f"""
Explain what changed in this commit and its impact:

{diff}
"""
    return ask_llm(prompt)


def get_current_branch():
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    )

    return f"Current branch: {result.stdout.strip()}"


def compare_branches(branch1, branch2):
    result = subprocess.run(
        ["git", "diff", f"{branch1}..{branch2}"],
        capture_output=True,
        text=True,
        cwd=REPO_PATH
    )

    diff = result.stdout.strip()

    if not diff:
        return f"No differences between {branch1} and {branch2}"

    prompt = f"""
Summarize the key differences between branches {branch1} and {branch2}:

{diff}
"""
    return ask_llm(prompt)


# =========================
# 🔹 FILE CONTENT HANDLER
# =========================

def explain_file(filename):
    full_path = os.path.join(REPO_PATH, filename)

    if not os.path.exists(full_path):
        return f"File {filename} not found."

    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    prompt = f"""
Explain what this file does briefly and clearly:

{code}
"""
    return ask_llm(prompt)


# =========================
# 🔹 INTENT ROUTER
# =========================

def handle_question(question):
    q = question.lower()

    # Who modified file
    if "who modified" in q:
        match = re.search(r"who modified (.+)", q)
        if match:
            filename = match.group(1).strip()
            return who_modified_file(filename)

    # Latest commits
    elif "latest commits" in q:
        return latest_commits()

    # Summarize commits
    elif "summarize commits" in q:
        return summarize_recent_commits()

    # Explain last commit
    elif "explain last commit" in q:
        return explain_last_commit_diff()

    # Current branch
    elif "current branch" in q:
        return get_current_branch()

    # Compare branches (basic parsing)
    elif "compare branches" in q:
        parts = q.split()
        if len(parts) >= 4:
            return compare_branches(parts[-2], parts[-1])
        else:
            return "Usage: compare branches branch1 branch2"

    # Explain file
    elif "what does" in q and ".c" in q:
        match = re.search(r"what does (.+) do", q)
        if match:
            filename = match.group(1).strip()
            return explain_file(filename)

    # Default → LLM reasoning
    else:
        return ask_llm(question)


# =========================
# 🔹 INTERACTIVE MODE
# =========================

if __name__ == "__main__":
    print("\n🚀 AI Git Assistant (type 'exit' to quit)\n")

    while True:
        question = input(">> ")

        if question.lower() == "exit":
            print("Goodbye.")
            break

        response = handle_question(question)
        print("\n" + response + "\n")
