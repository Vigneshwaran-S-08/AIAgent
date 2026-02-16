import subprocess
import sys
import os


# Ensure Ollama API is set
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"


MODEL_NAME = "ollama/deepseek-coder"  
# You can change to:
# "ollama/llama3"
# "ollama/mistral"


def run_aider(prompt):
    """
    Runs aider with a concise instruction wrapper
    """

    structured_prompt = f"""
You are a precise GitHub repository assistant.

Rules:
- Keep answers short and clear.
- Do not give long explanations.
- Answer only what is asked.
- If asking about a file, analyze only that file.
- If asking about changes, summarize briefly.

User Question:
{prompt}
"""

    cmd = [
        "aider",
        "--model", MODEL_NAME,
        "--no-auto-commits",      # prevent automatic git commits
        "--message", structured_prompt
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    return result.stdout


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python3 agent.py \"Your question here\"")
        sys.exit(1)

    query = sys.argv[1]

    response = run_aider(query)

    print("\n===== AI RESPONSE =====\n")
    print(response)
