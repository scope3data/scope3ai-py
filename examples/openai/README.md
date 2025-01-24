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
python openai-chat.py --model "gpt-4" --message "What is artificial intelligence?" --max-tokens 100

# Async streaming chat
python openai-async-stream-chat.py --model "gpt-4" --message "Explain quantum computing" --stream

# Generate an image
python openai-image.py --prompt "A beautiful sunset over mountains" --size "1024x1024"

# Async image generation
python openai-async-image.py --prompt "A futuristic city" --model "dall-e-3"

# Text to Speech
python openai-speech.py --text "Hello, welcome to the future!" --voice "alloy" --output speech.mp3

# Audio Transcription
python openai-transcription.py --file "recording.mp3" --model "whisper-1"
```