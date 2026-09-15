import json
import time
import urllib.request

OLLAMA_URL = "http://100.88.249.51:11434/api/generate"
MODEL = "qwen3-coder:30b"
CONTEXT = 32768
RUNS = 3

payload = {
    "model": MODEL,
    "prompt": "Write a Python function that checks whether a string is a palindrome.",
    "stream": False,
    "options": {
        "num_ctx": CONTEXT
    }
}

for run in range(1, RUNS + 1):
    start = time.perf_counter()

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request) as response:
        result = json.load(response)

    elapsed = time.perf_counter() - start

    eval_count = result.get("eval_count", 0)
    eval_duration = result.get("eval_duration", 0) / 1e9

    print(f"\nRun {run}")
    print(f"  Success:     {result.get('done')}")
    print(f"  Time:        {elapsed:.2f}s")
    print(f"  Tokens:      {eval_count}")
    print(f"  Ollama load: {result.get('load_duration', 0) / 1e9:.2f}s")
    print(f"  Ollama eval: {eval_duration:.2f}s")
    print(f"  Ollama tok/s: {eval_count / eval_duration:.2f}")
