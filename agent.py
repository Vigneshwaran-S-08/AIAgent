import requests
import subprocess
import sys
import os
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


# ----------------------------
# LLM CALL
# ----------------------------
def ask_llama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()


# ----------------------------
# INTENT DETECTION
# ----------------------------
def detect_intent(query):
    q = query.lower()

    if "who modified" in q or "history" in q or "commit" in q:
        return "history"

    if "explain" in q or "reason" in q or "what does" in q:
        return "explain"

    if "create" in q or "add" in q or "modify" in q or "update" in q:
        return "modify"

    return "unknown"


# ----------------------------
# FILE DETECTION
# ----------------------------
def detect_filename(query):
    match = re.search(r'\b[\w\-]+\.(c|cpp|py|h|java)\b', query)
    if match:
        return match.group(0)
    return None


# ----------------------------
# FILE OPERATIONS
# ----------------------------
def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return ""


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)


# ----------------------------
# GIT OPERATIONS
# ----------------------------
def git_commit(file_name, message):
    subprocess.run(["git", "add", file_name])
    subprocess.run(["git", "commit", "-m", message])


def get_file_history(filename):
    result = subprocess.run(
        ["git", "log",
         "--pretty=format:Commit ID: %H%nAuthor: %an%nDate: %ad%nMessage: %s%n---------------------------------------",
         "--", filename],
        capture_output=True,
        text=True
    )
    return result.stdout if result.stdout else "No history found."


# ----------------------------
# CODE EXPLANATION
# ----------------------------
def explain_file(filename):
    content = read_file(filename)

    if not content:
        return "File not found or empty."

    prompt = f"""
Explain the following code clearly and give reasoning of what it does.

Code:
{content}
"""

    return ask_llama(prompt)


# ----------------------------
# MAIN LOGIC
# ----------------------------
def main():

    if len(sys.argv) < 2:
        print("Usage: python3 agent.py \"Your request\"")
        return

    user_query = sys.argv[1]
    intent = detect_intent(user_query)
    file_name = detect_filename(user_query)

    if not file_name:
        print("❌ No filename detected in query.")
        return

    # ---------------- HISTORY MODE ----------------
    if intent == "history":
        history = get_file_history(file_name)
        print(f"\n📜 Modification History for {file_name}:\n")
        print(history)
        return

    # ---------------- EXPLAIN MODE ----------------
    if intent == "explain":
        explanation = explain_file(file_name)
        print(f"\n🧠 Code Explanation for {file_name}:\n")
        print(explanation)
        return

    # ---------------- MODIFY / CREATE MODE ----------------
    if intent == "modify":
        existing_content = read_file(file_name)

        prompt = f"""
You are a precise coding assistant.

Rules:
- Return ONLY raw code.
- No explanation.
- Complete file content.
- If file does not exist, create full new file.

Current file content:
{existing_content}

User request:
{user_query}
"""

        ai_output = ask_llama(prompt)

        write_file(file_name, ai_output)

        git_commit(file_name, f"AI update: {user_query}")

        print(f"\n✅ {file_name} updated and committed successfully.\n")
        return

    print("❌ Could not understand the request.")


if __name__ == "__main__":
    main()
