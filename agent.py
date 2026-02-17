import requests
import subprocess
import sys
import os
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


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


def detect_filename(query):
    """
    Detect filename like math_utils.c from query
    """
    match = re.search(r'\b[\w\-]+\.(c|cpp|py|h|java)\b', query)
    if match:
        return match.group(0)
    return None


def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return ""


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)


def git_commit(file_name, message):
    subprocess.run(["git", "add", file_name])
    subprocess.run(["git", "commit", "-m", message])


def main():

    if len(sys.argv) < 2:
        print("Usage: python3 agent.py \"Your request\"")
        return

    user_query = sys.argv[1]

    file_name = detect_filename(user_query)

    if not file_name:
        print("❌ No filename detected in query.")
        return

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


if __name__ == "__main__":
    main()
