# Benchmarking Documentation

This document describes our benchmarking methodology and results.

## Test Cases

We benchmark various scenarios including:
- Context window handling up to 16K tokens
- Tool calling performance
- Multi-turn conversation capacity

## Metrics

Key metrics include:
- Response latency
- Token throughput
- Memory usage
- Context budget utilization

## Results

The Ollama benchmark shows performance degradation at 16K tokens due to
increased attention computation requirements. We recommend staying under
8K tokens for optimal performance.

See `benchmarks/benchmark_results.md` for detailed results.
