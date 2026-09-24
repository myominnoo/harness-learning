#!/usr/bin/env python3
"""Lesson 01: connectivity & determinism baseline.

Every later lesson assumes two things about the local stack:
1. It's reachable and the target model is actually installed.
2. Generation at temperature=0 (+ fixed seed) is reproducible enough to
   build reliable evals on top of.

This script proves both, or fails loudly and says exactly what broke.
"""

from __future__ import annotations

import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://100.111.68.96:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:35b")
RUNS = int(os.getenv("DETERMINISM_RUNS", "5"))
PROMPT = "In one sentence, define what a tool call is in an LLM agent harness."


def request_json(path: str, payload: dict | None = None, timeout: int = 10) -> dict:
    url = f"{OLLAMA_URL}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def check(name: str, action):
    try:
        result = action()
        print(f"PASS  {name}: {result}")
        return True, result
    except Exception as error:
        print(f"FAIL  {name}: {error}")
        return False, None


def check_version() -> str:
    result = request_json("/api/version")
    version = result.get("version")
    if not version:
        raise RuntimeError("API returned no version")
    return version


def check_model() -> str:
    result = request_json("/api/tags")
    installed = {model.get("name") for model in result.get("models", [])}
    if MODEL not in installed:
        raise RuntimeError(f"{MODEL} not installed (have: {sorted(installed)})")
    return MODEL


def run_generation() -> tuple[str, float]:
    started = time.perf_counter()
    result = request_json(
        "/api/generate",
        {
            "model": MODEL,
            "prompt": PROMPT,
            "stream": False,
            "think": False,
            "options": {"temperature": 0, "seed": 42},
        },
        timeout=180,
    )
    elapsed = time.perf_counter() - started
    if not result.get("done"):
        raise RuntimeError("generation did not finish")
    return result.get("response", "").strip(), elapsed


def check_determinism() -> str:
    outputs = []
    latencies = []
    for i in range(RUNS):
        response, elapsed = run_generation()
        outputs.append(response)
        latencies.append(elapsed)
        print(f"      run {i + 1}/{RUNS}: {elapsed:.2f}s -> {response[:60]!r}")

    unique = set(outputs)
    latency_report = (
        f"latency min={min(latencies):.2f}s "
        f"mean={statistics.mean(latencies):.2f}s "
        f"max={max(latencies):.2f}s"
    )

    if len(unique) > 1:
        raise RuntimeError(
            f"{len(unique)}/{RUNS} distinct outputs at temperature=0, seed=42 "
            f"-- this model is not deterministic under these settings ({latency_report})"
        )

    return f"{RUNS}/{RUNS} identical outputs ({latency_report})"


def main() -> int:
    print("LESSON 01: CONNECTIVITY & DETERMINISM")
    print(f"Endpoint: {OLLAMA_URL}")
    print(f"Model:    {MODEL}")
    print(f"Runs:     {RUNS}")
    print()

    results = []
    ok, _ = check("Ollama API reachable", check_version)
    results.append(ok)

    ok, _ = check("Model installed", check_model)
    results.append(ok)

    if all(results):
        ok, _ = check("Deterministic generation", check_determinism)
        results.append(ok)
    else:
        print("SKIP  Deterministic generation: prerequisite checks failed")
        results.append(False)

    print()
    if all(results):
        print("RESULT: all checks passed -- safe to build evals assuming determinism")
        return 0

    print("RESULT: one or more checks failed")
    return 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.URLError as error:
        print(f"FAIL  Connection: {error}", file=sys.stderr)
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        raise SystemExit(130)
