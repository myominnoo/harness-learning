import json
import time
import urllib.request

OLLAMA_URL = "http://100.88.249.51:11434/api/generate"
MODEL = "qwen3-coder:30b"
NUM_CTX = 32768

FINAL_INSTRUCTION = "Write a Python function that checks whether a string is a palindrome."

FILLER_LINE = (
    "The quick brown fox jumps over the lazy dog while the river flows steadily "
    "beneath the old stone bridge near the quiet village at the edge of the woods. "
)

# V6 experiment: isolate whether increasing prompt/context content affects completion speed.
# Use reduced target set: [2000, 8000, 16000] tokens.
TARGET_TOKENS = [2000, 8000, 16000]
RUNS = 3
CHARS_PER_TOKEN = 5.09

print(f"V6 experiment: {MODEL} num_ctx={NUM_CTX}")
print(f"Runs per target: {RUNS}")
print("=" * 40)

for target_tokens in TARGET_TOKENS:
    char_target = int(target_tokens * CHARS_PER_TOKEN)

    filler = FILLER_LINE * (char_target // len(FILLER_LINE) + 1)
    filler = filler[:char_target]
    prompt = f"{filler}\n\n{FINAL_INSTRUCTION}"
    estimated_chars = len(prompt)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": NUM_CTX
        }
    }

    print(f"--- Target: ~{target_tokens} tokens (est. {estimated_chars} chars) ---")

    completion_toks_per_sec_list = []
    prompt_toks_per_sec_list = []

    for run_num in range(1, RUNS + 1):
        print(f"  Run {run_num}/{RUNS}...")

        start = time.perf_counter()
        success = False
        result = {}

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
            print(f"  Error: {error}")
            print("-" * 40)
            continue

        elapsed = time.perf_counter() - start

        eval_count = result.get("eval_count", 0)
        eval_duration = result.get("eval_duration", 0) / 1e9
        tokens_per_sec = (
            eval_count / eval_duration
            if eval_duration
            else 0.0
        )

        prompt_eval_count = result.get("prompt_eval_count", 0)
        prompt_eval_duration = result.get("prompt_eval_duration", 0) / 1e9
        prompt_tok_per_sec = (
            prompt_eval_count / prompt_eval_duration
            if prompt_eval_duration
            else 0.0
        )

        load_duration = result.get("load_duration", 0) / 1e9

        print(f"  Target Tokens:      {target_tokens}")
        print(f"  Estimated Chars:    {estimated_chars}")
        print(f"  Actual Prompt Eval: {prompt_eval_count}")
        print(f"  P Eval Duration:    {prompt_eval_duration:.2f}s")
        print(f"  P Eval Tok/s:       {prompt_tok_per_sec:.2f}")
        print(f"  Load Duration:      {load_duration:.2f}s")
        print(f"  Eval Count:         {eval_count}")
        print(f"  Eval Duration:      {eval_duration:.2f}s")
        print(f"  Completion Tok/s:   {tokens_per_sec:.2f}")
        print(f"  Total Elapsed:      {elapsed:.2f}s")
        print(f"  Success:            {success}")
        print("-" * 40)

        if success:
            completion_toks_per_sec_list.append(tokens_per_sec)
            prompt_toks_per_sec_list.append(prompt_tok_per_sec)

    if completion_toks_per_sec_list:
        avg_completion_toks = (
            sum(completion_toks_per_sec_list)
            / len(completion_toks_per_sec_list)
        )
        avg_prompt_toks = (
            sum(prompt_toks_per_sec_list)
            / len(prompt_toks_per_sec_list)
        )

        print(
            f"  Successful runs:    "
            f"{len(completion_toks_per_sec_list)}/{RUNS}"
        )
        print(f"  Avg Completion Tok/s: {avg_completion_toks:.2f}")
        print(f"  Avg Prompt Tok/s:     {avg_prompt_toks:.2f}")
    else:
        print("  No successful runs for this target.")

    print("=" * 40)
