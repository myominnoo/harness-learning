# System Architecture Overview

This project implements an AI agent with context-aware selection capabilities.

## Core Components

The main components include:
- Agent loop for processing requests
- Context selector for file relevance ranking
- Tool registry for available capabilities
- Verification system for output quality

## Context Management

Context budgeting is used to limit the amount of text fed to the model.
The context selector scores files based on keyword matching and ranks them
by relevance to the current query.

## Performance Considerations

Token limits are critical for performance. We aim to stay under 16K tokens
for most use cases while maintaining response quality.
