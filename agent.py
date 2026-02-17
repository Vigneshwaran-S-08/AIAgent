import requests
import subprocess
import sys
import os

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

    return response.json()["response"]


def read_file(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r") as f:
        return f.read()


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)


def git_commit(message):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 agent.py \"Your request\"")
        return

    user_query = sys.argv[1]

    # Example: operate on hello.c
    file_name = "hello.c"

    file_content = read_file(file_name)

    prompt = f"""
You are a precise coding assistant.

Rules:
- Return only updated code.
- No explanations.
- Keep code clean.

Current file content:
{file_content}

User request:
{user_query}
"""

    ai_output = ask_llama(prompt)

    write_file(file_name, ai_output)

    git_commit(f"AI update: {user_query}")

    print("\nUpdated and committed successfully.\n")


if __name__ == "__main__":
    main()
