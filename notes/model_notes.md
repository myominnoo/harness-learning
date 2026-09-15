# Model Notes

Notes on model selection and configuration.

## Supported Models

- llama2: Generic assistant model
- mistral: Efficient inference
- gemma: Google's open model

## Configuration

Models are configured in `config/models.yaml`.

## Context Windows

Each model has different context window sizes:
- llama2: 16K tokens
- mistral: 8K tokens
- gemma: 8K tokens

## Recommendations

For benchmarking, use llama2 with consistent parameters.
Monitor token usage to avoid exceeding context limits.
