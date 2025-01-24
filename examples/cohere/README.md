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
python cohere-chat.py --message "What is machine learning?" --max-tokens 100

# With custom API key
python cohere-chat.py --message "Explain neural networks" --api-key "your-api-key"


python cohere_v2-stream-chat.py --model "command-r-plus-08-2024" --message "Write a story about AI"

# Async streaming
python cohere_v2-async-stream-chat.py --message "Explain quantum mechanics" --max-tokens 200
```