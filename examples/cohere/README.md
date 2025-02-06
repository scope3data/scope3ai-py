# Cohere Examples with Scope3AI

This directory contains examples of using Cohere's API with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat Completion (v1)
- `cohere-chat.py` - Basic chat completion
- `cohere-async-chat.py` - Asynchronous chat completion
- `cohere-stream-chat.py` - Streaming chat completion
- `cohere-async-stream-chat.py` - Asynchronous streaming chat completion

### Chat Completion (v2)
- `cohere_v2-chat.py` - Basic chat completion
- `cohere_v2-async-chat.py` - Asynchronous chat completion
- `cohere_v2-stream-chat.py` - Streaming chat completion
- `cohere_v2-async-stream-chat.py` - Asynchronous streaming chat completion

## Usage Examples

### Basic Chat (v1)
```bash
uv run python -m examples.cohere.cohere-chat --message "What is machine learning?" --max-tokens 100

uv run python -m examples.cohere.cohere-async-chat --message "Explain neural networks" --max-tokens 200

uv run python -m examples.cohere.cohere-stream-chat --message "Write a story about AI"

uv run python -m examples.cohere.cohere-async-stream-chat --message "Explain quantum mechanics" --max-tokens 200
```

### Basic Chat (v2)
```bash
uv run python -m examples.cohere.cohere_v2-chat --message "What is machine learning?" --max-tokens 100

uv run python -m examples.cohere.cohere_v2-async-chat --message "Explain neural networks" --max-tokens 200

uv run python -m examples.cohere.cohere_v2-stream-chat --message "Write a story about AI"

uv run python -m examples.cohere.cohere_v2-async-stream-chat --message "Explain quantum mechanics" --max-tokens 200
```