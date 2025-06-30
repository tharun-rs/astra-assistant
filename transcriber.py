# transcriber.py
import subprocess

def transcribe(filename="command.wav", model="base.en"):
    result = subprocess.run(
        ["./whisper.cpp/main", "-m", f"./whisper.cpp/models/ggml-{model}.bin", "-f", filename],
        capture_output=True, text=True
    )
    lines = result.stdout.splitlines()
    for line in lines[::-1]:
        if line.strip().startswith("[") and "]" in line:
            return line.split("]", 1)[-1].strip()
    return ""
