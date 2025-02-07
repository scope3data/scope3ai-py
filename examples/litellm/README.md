# LiteLLM Examples with Scope3AI

This directory contains examples of using LiteLLM with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat & Completion
- `litellm-completion.py` - Basic completion
- `litellm-acompletion.py` - Asynchronous completion

### Image Generation
- `litellm-image-generation.py` - Image generation
- `litellm-aimage-generation.py` - Asynchronous image generation

### Speech & Audio
- `litellm-speech.py` - Text to speech conversion
- `litellm-aspeech.py` - Asynchronous text to speech
- `litellm-transcription.py` - Speech to text transcription
- `litellm-atranscription.py` - Asynchronous transcription

## Usage Examples

### Completion
```bash
uv run python -m examples.litellm.litellm-completion --model "gpt-4" --message "What is artificial intelligence?"

uv run python -m examples.litellm.litellm-acompletion --model "gpt-4" --message "Explain quantum computing" --max-tokens 200

uv run python -m examples.litellm.litellm-image-generation --prompt "A beautiful sunset" --size "1024x1024"

uv run python -m examples.litellm.litellm-aimage-generation --prompt "A beautiful sunset" --size "1024x1024"

uv run python -m examples.litellm.litellm-speech --text "Hello world" --voice "alloy"

uv run python -m examples.litellm.litellm-aspeech --text "Hello world" --voice "alloy"

uv run python -m examples.litellm.litellm-transcription --audio-path "recording.wav" --model "whisper-1"

uv run python -m examples.litellm.litellm-atranscription --audio-path "recording.wav" --model "whisper-1"
```