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
python litellm-completion.py --model "gpt-4" --message "What is artificial intelligence?"

python litellm-acompletion.py --message "Explain quantum computing" --max-tokens 200

python litellm-image-generation.py --prompt "A beautiful sunset" --size "1024x1024"

python litellm-speech.py --text "Hello world" --voice "alloy"

python litellm-transcription.py --audio-path "recording.wav" --model "whisper-1"
```