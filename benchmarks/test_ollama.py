import json
import time
import urllib.request

OLLAMA_URL = "http://100.88.249.51:11434/api/generate"
MODEL = "qwen3-coder:30b"
NUM_CTX = 32768

FINAL_INSTRUCTION = "Write a Python function that checks whether a string is a palindrome."

# V4 experiment: build a deterministic, long prompt locally (no manual pasting).
# Target roughly 8,000 input tokens (~1 token per ~4 chars -> ~32,000 chars)
# before the final instruction.
TARGET_CHAR_COUNT = 32000
FILLER_LINE = (
    "The quick brown fox jumps over the lazy dog while the river flows steadily "
    "beneath the old stone bridge near the quiet village at the edge of the woods. "
)

filler = FILLER_LINE * (TARGET_CHAR_COUNT // len(FILLER_LINE) + 1)
filler = filler[:TARGET_CHAR_COUNT]

prompt = f"{filler}\n\n{FINAL_INSTRUCTION}"

payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": {
        "num_ctx": NUM_CTX
    }
}

print(f"V4 experiment: {MODEL} num_ctx={NUM_CTX}")
print(f"  Prompt chars:   {len(prompt)}")

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
    print(f"  Success:     False")
    print(f"  Error:       {error}")

elapsed = time.perf_counter() - start

# Output token metrics (completion, existing measurement).
eval_count = result.get("eval_count", 0)
eval_duration = result.get("eval_duration", 0) / 1e9
tokens_per_sec = eval_count / eval_duration if eval_duration else 0.0

# Prefill metrics: how many prompt tokens Ollama actually processed, and for how long.
prompt_eval_count = result.get("prompt_eval_count", 0)
prompt_eval_duration = result.get("prompt_eval_duration", 0) / 1e9

print(f"  Success:     {success}")
print(f"  Time:        {elapsed:.2f}s")
print(f"  Ollama load: {result.get('load_duration', 0) / 1e9:.2f}s")
print(f"  Ollama prompt_eval_count:   {prompt_eval_count}")
print(f"  Ollama prompt_eval_duration: {prompt_eval_duration:.2f}s")
print(f"  Tokens:      {eval_count}")
print(f"  Ollama eval: {eval_duration:.2f}s")
print(f"  Ollama tok/s: {tokens_per_sec:.2f}")
