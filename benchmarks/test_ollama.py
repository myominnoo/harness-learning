import json
import time
import urllib.request

OLLAMA_URL = "http://100.88.249.51:11434/api/generate"
MODEL = "qwen3-coder:30b"
CONTEXT_SIZES = [32768, 65536, 131072, 196608, 262144]

prompt = "Write a Python function that checks whether a string is a palindrome."

for context in CONTEXT_SIZES:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": context
        }
    }

    start = time.perf_counter()
    success = False

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(request) as response:
            result = json.load(response)
        success = bool(result.get("done"))
    except Exception as error:
        result = {}
        print(f"\nContext: {context}")
        print(f"  Success:     False")
        print(f"  Error:       {error}")
        continue

    elapsed = time.perf_counter() - start
    eval_count = result.get("eval_count", 0)
    eval_duration = result.get("eval_duration", 0) / 1e9
    tokens_per_sec = eval_count / eval_duration if eval_duration else 0.0

    print(f"\nContext: {context}")
    print(f"  Success:     {success}")
    print(f"  Time:        {elapsed:.2f}s")
    print(f"  Tokens:      {eval_count}")
    print(f"  Ollama load: {result.get('load_duration', 0) / 1e9:.2f}s")
    print(f"  Ollama eval: {eval_duration:.2f}s")
    print(f"  Ollama tok/s: {tokens_per_sec:.2f}")
