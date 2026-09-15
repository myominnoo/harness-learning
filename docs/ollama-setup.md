# Ollama Setup Guide

Ollama provides a simple way to run open-source LLMs locally.

## Installation

Download Ollama from the official website and install it.

```bash
curl https://ollama.com/install.sh | sh
```

## Configuration

Set up your model paths and context limits in the configuration file.
The default context window is 16K tokens but can be adjusted.

## Usage

Run Ollama with the desired model:
```bash
ollama run llama2
```

For benchmarking, use consistent parameters to ensure reliable comparisons.
