# Agent Loop

The agent loop processes user requests and generates responses.

## Workflow

1. Receive input
2. Select relevant context
3. Generate response using the model
4. Verify output quality
5. Return result

## Context Selection

We use keyword-based context selection to find relevant files.
The selected context is passed to the model along with the query.

## Performance

The loop handles multiple concurrent requests while maintaining
context budget limitations.
