# Lesson 01: Connectivity & Determinism Baseline

## Why this comes first

Every later lesson in this curriculum — tool-calling reliability,
context-truncation evals, plan/verify loops — depends on one assumption:
that repeating the same prompt at `temperature=0` against your local model
gives you the same answer back. If that assumption is false, every eval
built on top of it is measuring noise, not the harness.

This lesson tests the assumption instead of asserting it.

## What it checks

1. The Ollama API on your OneXStation is reachable over Tailscale.
2. The target model is actually installed there.
3. The same prompt, run `N` times with `temperature=0` and a fixed `seed`,
   produces byte-identical output. Latency is recorded on every run
   regardless of outcome.

## Running it

```bash
export OLLAMA_URL="http://<your-tailscale-ip>:11434"   # default: http://100.111.68.96:11434
export OLLAMA_MODEL="qwen3.5:35b"                        # default: qwen3.5:35b
export DETERMINISM_RUNS=5                                # default: 5

python3 check_stack.py
```

Exit code `0` means all three checks passed. Anything else means don't
trust downstream evals against this model/endpoint until you know why.

## What "fail" here actually teaches you

If the determinism check fails, that's not a bug in the script — it's a
real finding about your stack (many local runtimes batch requests in ways
that make `temperature=0` non-deterministic across concurrent load). Note
the failure mode and how many runs diverged; later lessons that build
evals around exact-match will need to account for it (e.g. by running
single-request, unbatched, or by widening comparisons to semantic
equivalence instead of string equality).
