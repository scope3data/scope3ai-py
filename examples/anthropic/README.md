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
python anthropic-chat.py --model "claude-3-sonnet-latest" --message "What is machine learning?" --max-tokens 100

# With custom API key
python anthropic-chat.py --message "Explain neural networks" --api-key "your-api-key"

# Streaming Chat
python anthropic-stream-chat.py --message "Write a story about AI" --model "claude-3-opus-latest"

# Async streaming
python anthropic-async-stream-chat.py --message "Explain quantum mechanics" --max-tokens 200
```