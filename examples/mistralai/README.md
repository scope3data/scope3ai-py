# Mistral AI Examples with Scope3AI

This directory contains examples of using Mistral AI's API with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat Completion
- `mistral-complete.py` - Basic completion
- `mistral-complete-async.py` - Asynchronous completion
- `mistral-stream.py` - Streaming completion
- `mistral-stream-async.py` - Asynchronous streaming completion

## Usage Examples

```bash
python mistral-complete.py --model "mistral-large-latest" --message "What is artificial intelligence?" --max-tokens 100

# With custom temperature
python mistral-complete.py --message "Write a story" --temperature 0.9

python mistral-stream.py --message "Explain quantum mechanics" --max-tokens 200

# Async streaming
python mistral-stream-async.py--model "mistral-medium" --message "Tell me a story"
```