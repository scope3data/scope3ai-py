# Anthropic Claude Examples with Scope3AI

This directory contains examples of using Anthropic's Claude API with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat Completion
- `anthropic-chat.py` - Basic chat completion
- `anthropic-async-chat.py` - Asynchronous chat completion
- `anthropic-stream-chat.py` - Streaming chat completion
- `anthropic-async-stream-chat.py` - Asynchronous streaming chat completion

## Usage Examples


```bash
# Basic Chat
uv run python -m examples.anthropic.anthropic-chat --model "claude-3-opus-latest" --message "What is machine learning?" --max-tokens 100

# Async Chat
uv run python -m examples.anthropic.anthropic-async-chat --model "claude-3-opus-latest" --message "What is machine learning?" --max-tokens 100

# Streaming Chat
uv run python -m examples.anthropic.anthropic-stream-chat --model "claude-3-opus-latest" --message "Write a story about AI"

# Async streaming
uv run python -m examples.anthropic.anthropic-async-stream-chat --model "claude-3-opus-latest" --message "Explain quantum mechanics" --max-tokens 200
```