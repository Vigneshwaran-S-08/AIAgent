import subprocess

MODEL_NAME = "deepseek-coder:6.7b"

def ask_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )

    return result.stdout.decode()
