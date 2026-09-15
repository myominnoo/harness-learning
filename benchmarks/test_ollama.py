import json
import time
import urllib.request

OLLAMA_URL = "http://100.88.249.51:11434/api/generate"
MODEL = "qwen3-coder:30b"
CONTEXT = 32768

payload = {
    "model": MODEL,
    "prompt": "Write a Python function that checks whether a string is a palindrome.",
    "stream": False,
    "options": {
        "num_ctx": CONTEXT
    }
}

start = time.perf_counter()

request = urllib.request.Request(
    OLLAMA_URL,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
)

with urllib.request.urlopen(request) as response:
    result = json.load(response)

elapsed = time.perf_counter() - start

print(f"Model:       {MODEL}")
print(f"Context:     {CONTEXT:,}")
print(f"Success:     {result.get('done')}")
print(f"Time:        {elapsed:.2f}s")
print(f"Tokens:      {result.get('eval_count')}")
print(f"Tokens/sec:  {result.get('eval_count', 0) / elapsed:.2f}")
print(f"Ollama load: {result.get('load_duration', 0) / 1e9:.2f}s")
print(f"Ollama eval: {result.get('eval_duration', 0) / 1e9:.2f}s")
print(f"Ollama tok/s: {result.get('eval_count', 0) / (result.get('eval_duration', 1) / 1e9):.2f}")
