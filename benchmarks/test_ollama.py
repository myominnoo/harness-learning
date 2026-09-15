#!/usr/bin/env python3
"""
Ollama benchmark testing script.
"""

import subprocess
import time


def run_benchmark(model: str, context_size: int) -> float:
    """Run a benchmark with given context size."""
    start = time.time()
    cmd = ["ollama", "run", model]
    
    # Simulate context
    context = "x" * context_size
    
    proc = subprocess.run(
        cmd,
        input=context,
        capture_output=True,
        text=True
    )
    
    return time.time() - start


def main():
    """Run benchmarks for different context sizes."""
    for size in [1024, 4096, 8192, 16384]:
        elapsed = run_benchmark("llama2", size)
        print(f"Context: {size}, Time: {elapsed:.3f}s")


if __name__ == "__main__":
    main()
