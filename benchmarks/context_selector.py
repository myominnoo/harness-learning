#!/usr/bin/env python3
"""
Simple context selector using keyword matching.
No LLM, embeddings, or external libraries used.
"""
import re
from collections import Counter

# Define the list of files to search
FILES = [
    "README.md",
    "benchmarks/test_ollama.py",
    "benchmarks/test_short.md",
    "benchmarks/test_long.md",
    "notes/context_budgeting.md",
    "docs/setup.md",
    "data/results.csv",
]

# Define the query
QUERY = "Explain why the Ollama benchmark slows down at 16K tokens."

# Maximum number of files to select
MAX_FILES = 2


def select_files(files, query):
    """
    Select files relevant to the query using weighted keyword scoring.
    Returns a list of (filename, normalized_score, raw_score, word_count, matched_keywords)
    tuples sorted by normalized score descending.
    """
    # Stopwords to exclude from keyword extraction
    stopwords = {
        "the", "why", "does", "down", "at", "and", "how", "is", "a", "an", "to", "of", "for"
    }
    
    # Extract keywords from the query using proper tokenization
    # Filter out stopwords and tokens shorter than 4 characters
    keywords = [
        word for word in re.findall(r"[a-z0-9]+", query.lower())
        if word not in stopwords and len(word) >= 3
    ]
    
    # Weight each keyword by specificity
    keyword_weights = {
        "ollama": 3,
        "benchmark": 3,
        "16k": 3,
        "tokens": 1,
    }
    
    scores = []
    
    for filename in files:
        # Read file content
        try:
            with open(filename, 'r') as f:
                text_lower = f.read().lower()
        except FileNotFoundError:
            continue

        # Tokenize the document using regex (alphanumeric-only tokens)
        tokens = re.findall(r"[a-z0-9]+", text_lower)
        word_count = max(len(tokens), 1)

        # Count whole-word occurrences using Counter
        token_counts = Counter(tokens)

        score = 0
        matched = {}
        for keyword in keywords:
            count = token_counts.get(keyword, 0)

            if count > 0:
                weight = keyword_weights.get(keyword, 1)
                score += count * weight
                matched[keyword] = count * weight

        normalized_score = score / (word_count ** 0.5)
    
        if score > 0:
            scores.append((filename, normalized_score, score, word_count, list(matched.items())))
    
    # Sort by score from highest to lowest
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores


def main():
    """Main function to demonstrate context selection."""
    results = select_files(FILES, QUERY)
    
    print("Files ranked by keyword score:")
    for filename, score, raw_score, word_count, matched_keywords in results:
        print(f"{score:.2f}: {filename}")
        print(f"    Raw score: {raw_score}")
        print(f"    Words: {word_count}")
        for keyword, weight in matched_keywords:
            print(f"    {keyword}: {weight}")
    
    print("\nSelected for context:")
    for filename, *rest in results[:MAX_FILES]:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()
