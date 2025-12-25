# transcriber.py
import subprocess

def transcribe(filename="command.wav", model="tiny.en"):
    result = subprocess.run(
        ["./whisper.transcriber/whisper-cli", "-m", f"./whisper.transcriber/ggml-{model}.bin", "-f", filename],
        capture_output=True, text=True
    )
    lines = result.stdout.splitlines()
    for line in lines[::-1]:
        if line.strip().startswith("[") and "]" in line:
            return line.split("]", 1)[-1].strip()
    return ""
