# Experiments Log

Documenting experiments and their results.

## Experiment 1: Context Size vs Performance

We tested different context sizes to measure performance impact.

### Results

Performance degrades significantly at 16K tokens.
The attention mechanism becomes the bottleneck.

### Conclusion

Stay under 8K tokens for optimal performance.

## Experiment 2: Keyword Selection

Testing simple keyword matching vs more complex approaches.

### Results

Keyword matching works well for our use case.
It's simple and fast with good recall.

### Conclusion

Keep the simple keyword-based selector.
