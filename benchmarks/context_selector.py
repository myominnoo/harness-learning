#!/usr/bin/env python3
"""
Simple context selector using TF-IDF scoring.
No LLM, embeddings, or external libraries used.
"""
import math
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
    Select files relevant to the query using TF-IDF scoring.
    Returns a list of (filename, normalized_score, raw_score) tuples sorted by score descending.
    """
    # Stopwords to exclude from keyword extraction
    stopwords = {
        "the", "why", "does", "down", "at", "and", "how", "is", "a", "an", "to", "of", "for"
    }
    
    # Extract keywords from the query using proper tokenization
    keywords = [
        word for word in re.findall(r"[a-z0-9]+", query.lower())
        if word not in stopwords and len(word) >= 3
    ]
    
    scores = []
    temp_data = []
    
    # First pass: calculate document frequency (df) for each keyword across all files,
    # and count total valid documents (N).
    total_docs = 0
    doc_freqs = {}
    
    for filename in files:
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
        
        temp_data.append((filename, word_count, token_counts))
        total_docs += 1
        
        for kw in keywords:
            if token_counts.get(kw, 0) > 0:
                doc_freqs[kw] = doc_freqs.get(kw, 0) + 1

    # Second pass: Calculate TF-IDF scores with length normalization
    for filename, word_count, token_counts in temp_data:
        score = 0.0
        keyword_stats = {}
        
        for kw in keywords:
            tf = token_counts.get(kw, 0)
            
            if tf > 0:
                df = doc_freqs[kw]
                
                # Calculate IDF
                idf = math.log((total_docs + 1) / (df + 1)) + 1
                
                # Calculate TF-IDF Contribution
                tfidf_val = tf * idf
                
                score += tfidf_val
                keyword_stats[kw] = {"tf": tf, "df": df, "idf": idf, "tfidf": tfidf_val}

        normalized_score = score / (word_count ** 0.5)
        
        scores.append((filename, normalized_score, score, keyword_stats))
    
    # Sort by normalized score from highest to lowest
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores


def main():
    """Main function to demonstrate context selection."""
    results = select_files(FILES, QUERY)
    
    print("Files ranked by TF-IDF score:")
    for filename, norm_score, raw_score, kw_stats in results:
        print(f"{norm_score:.2f}: {filename}")
        print(f"    Raw TF-IDF score: {raw_score:.2f}")
        
        # Explainable breakdown of keyword contribution
        for kw, stats in kw_stats.items():
            print(f"    {kw}:")
            print(f"        TF: {stats['tf']}")
            print(f"        DF: {stats['df']}")
            print(f"        IDF: {stats['idf']:.2f}")
            print(f"        TF-IDF: {stats['tfidf']:.2f}")
    
    print("\nSelected for context:")
    for filename, *rest in results[:MAX_FILES]:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()
