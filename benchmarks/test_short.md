# Ollama benchmark notes

An Ollama benchmark run shows that inference latency grows as the context window approaches 16K tokens. Short prompts stay fast, and small prompts complete quickly, but the same benchmark gets progressively slower once input passes 16K. A repeat run confirms the pattern.
