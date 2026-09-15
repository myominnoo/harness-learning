# Context Management

Effective context management is crucial for AI agent performance.

## Context Budgeting

We implement context budgeting to ensure we stay within token limits.
The budget is divided among:
- System prompt
- User input
- History
- Retrieved context

## Retrieval Strategy

Our retrieval system uses keyword matching to select relevant files.
Files are scored based on keyword presence and sorted by relevance.

## Best Practices

- Keep context windows under 8K for reliable performance
- Use context budgeting to prevent overflow
- Prioritize relevant context to improve signal-to-noise ratio
