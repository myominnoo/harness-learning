# Agent Prompts

This document describes the prompt templates used by the agent.

## System Prompt

The system prompt sets the agent's behavior and capabilities.

## User Prompt Structure

Each user prompt includes:
- Query or request
- Selected context from file search
- Any relevant tool descriptions

## Prompt Best Practices

- Keep prompts concise and focused
- Include only relevant context to stay under token limits
- Use clear instructions for better model performance

## Example

```python
prompt = f"""
System: You are a helpful AI assistant.

Context:
{context}

User: {query}
"""
```
