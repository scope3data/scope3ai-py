# Mistral AI Examples with Scope3AI

This directory contains examples of using Mistral AI's API with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat Completion
- `mistral-complete.py` - Basic completion
- `mistral-complete-async.py` - Asynchronous completion
- `mistral-stream.py` - Streaming completion
- `mistral-stream-async.py` - Asynchronous streaming completion

## Usage Examples

From the root directory, run the following commands:

```bash
uv run python -m examples.mistralai.mistral-complete --model "mistral-large-latest" --message "What is artificial intelligence?" --max-tokens 100

# With custom temperature
uv run python -m examples.mistralai.mistral-complete --message "Write a story" --temperature 0.9

uv run python -m examples.mistralai.mistral-stream --message "Explain quantum mechanics" --max-tokens 200

# Async streaming
uv run python -m examples.mistralai.mistral-stream-async --model "mistral-medium" --message "Tell me a story"
```