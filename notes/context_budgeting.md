# Context Budgeting Notes

Our context budgeting system ensures we stay within token limits.

## Budget Allocation

Total context budget: 16K tokens
- System prompt: 512 tokens
- User input: 2048 tokens
- History: 4096 tokens
- Retrieved context: 9440 tokens

## Budget Management

The context selector helps manage budgets by:
1. Scoring files based on relevance
2. Ranking by keyword matches
3. Limiting selected files to MAX_FILES

## Optimization

We optimize for:
- Maximum relevance within budget
- Minimal token waste
- Consistent performance
