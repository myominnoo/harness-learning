# Benchmark Results

This file contains detailed benchmark results.

## Test Parameters

- Models: llama2, mistral, gemma
- Context sizes: 1K, 4K, 8K, 16K tokens
- Workload: Mixed tool calling and generation

## Results Summary

| Context Size | Latency (ms) | Throughput (tok/s) |
|--------------|--------------|-------------------|
| 1K           | 150          | 250               |
| 4K           | 180          | 220               |
| 8K           | 220          | 190               |
| 16K          | 350          | 140               |

## Analysis

Performance degrades significantly at 16K tokens. The attention mechanism
becomes the bottleneck as sequence length increases quadratically.

## Recommendations

- Use context budgeting to stay under 8K tokens
- Implement smart context selection
- Consider model quantization for better performance
