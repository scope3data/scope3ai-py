# OpenAI Examples with Scope3AI

This directory contains examples of using OpenAI's API with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat Completion
- `openai-chat.py` - Basic chat completion
- `openai-async-chat.py` - Asynchronous chat completion
- `openai-stream-chat.py` - Streaming chat completion
- `openai-async-stream-chat.py` - Asynchronous streaming chat completion

### Image Generation
- `openai-image.py` - Image generation
- `openai-async-image.py` - Asynchronous image generation

### Speech & Audio
- `openai-speech.py` - Text-to-speech conversion
- `openai-async-speech.py` - Asynchronous text-to-speech
- `openai-transcription.py` - Speech-to-text transcription
- `openai-async-transcription.py` - Asynchronous transcription

## Usage Examples

```bash
# Basic chat
uv run python -m examples.openai.openai-chat --model "gpt-4" --message "What is artificial intelligence?"

# Async streaming chat
uv run python -m examples.openai.openai-async-stream-chat --model "gpt-4" --message "Explain quantum computing"

# Generate an image
uv run python -m examples.openai.openai-image --prompt "A beautiful sunset over mountains" --model "dall-e-2" --size "1024x1024"

# Async image generation
uv run python -m examples.openai.openai-async-image --prompt "A futuristic city" --model "dall-e-2" --size "1024x1024"

# Text to Speech
uv run python -m examples.openai.openai-speech --text "Hello, welcome to the future!" --model "tts-1" --response-format "mp3"

# Async Text to Speech
uv run python -m examples.openai.openai-async-speech --text "Hello, welcome to the future!" --model "tts-1" --response-format "mp3"

# Audio Transcription
uv run python -m examples.openai.openai-transcription --filename "recording.mp3" --model "whisper-1"

# Async Audio Transcription
uv run python -m examples.openai.openai-async-transcription --filename "recording.mp3" --model "whisper-1"
```