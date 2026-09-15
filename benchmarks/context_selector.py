#!/usr/bin/env python3
"""
Simple context selector using keyword matching.
No LLM, embeddings, or external libraries used.
"""

# Define the list of files to search
FILES = [
    "README.md",
    "benchmarks/test_ollama.py",
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
    Returns a list of (filename, score, matched_keywords) tuples sorted by score descending.
    """
    # Stopwords to exclude from keyword extraction
    stopwords = {
        "the", "why", "does", "down", "at", "and", "how", "is", "a", "an", "to", "of", "for"
    }
    
    # Extract keywords from the query by splitting and filtering
    # Filter out stopwords and words shorter than 4 characters
    keywords = [
        word for word in query.lower().split()
        if word not in stopwords and len(word) > 3
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
        # Skip files that don't exist
        try:
            with open(filename, 'r') as f:
                content = f.read().lower()
        except FileNotFoundError:
            continue
        
        # Find matched keywords and calculate weighted score
        matched_keywords = []
        for keyword in keywords:
            if keyword in content:
                matched_keywords.append((keyword, keyword_weights.get(keyword, 1)))
        
        score = sum(weight for _, weight in matched_keywords)
        
        if score > 0:
            scores.append((filename, score, matched_keywords))
    
    # Sort by score from highest to lowest
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores


def main():
    """Main function to demonstrate context selection."""
    results = select_files(FILES, QUERY)
    
    print("Files ranked by keyword score:")
    for filename, score, matched_keywords in results:
        print(f"  {score}: {filename}")
        for keyword, weight in matched_keywords:
            print(f"     {keyword}: {weight}")
    
    print("\nSelected for context:")
    for filename, score, _ in results[:MAX_FILES]:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()
