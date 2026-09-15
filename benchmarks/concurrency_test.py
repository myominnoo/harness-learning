#!/usr/bin/env python3
"""Concurrency test for benchmarking."""

import asyncio
import time


async def run_benchmark(tasks: int, context_size: int) -> float:
    """Run concurrent benchmarks."""
    start = time.time()
    
    async def task():
        await asyncio.sleep(0.01)
        return True
    
    results = await asyncio.gather(*[task() for _ in range(tasks)])
    return time.time() - start


def main():
    """Run concurrency tests."""
    for tasks in [1, 2, 4, 8]:
        elapsed = asyncio.run(run_benchmark(tasks, 8192))
        print(f"Tasks: {tasks}, Time: {elapsed:.3f}s")


if __name__ == "__main__":
    main()
