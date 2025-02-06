# HuggingFace Examples with Scope3AI

This directory contains examples of using HuggingFace's Inference API with environmental impact tracking via Scope3AI.

## Scripts Overview

### Chat
- `chat.py` - Basic chat completion
- `chat-async.py` - Asynchronous chat completion

### Image Processing
- `image-to-image.py` - Image transformation
- `image-to-image-async.py` - Asynchronous image transformation

### Speech & Audio
- `speech-to-text.py` - Audio transcription
- `speech-to-text-async.py` - Asynchronous audio transcription
- `text-to-speech.py` - Text to speech conversion
- `text-to-speech-async.py` - Asynchronous text to speech

### Translation & Text Generation
- `translation.py` - Text translation
- `translation-async.py` - Asynchronous translation
- `text-to-image.py` - Text to image generation
- `text-to-image-async.py` - Asynchronous text to image generation

## Usage Examples

```bash
# chat
uv run python -m examples.hugging-face.chat --message "Explain the theory of relativity" --max-tokens 100

# chat async
uv run python -m examples.hugging-face.chat-async --message "What is quantum computing?"

# speech & Audio
uv run python -m examples.hugging-face.speech-to-text --audio-path "recording.wav"

# speech & Audio async
uv run python -m examples.hugging-face.text-to-speech --text "Hello world!"

# translation
uv run python -m examples.hugging-face.translation --text "Hello, how are you?" --target-language "es"

# text to image
uv run python -m examples.hugging-face.text-to-image --prompt "A beautiful sunset over mountains" --model "dall-e-2" --size "1024x1024"

# text to image async
uv run python -m examples.hugging-face.text-to-image-async --prompt "A futuristic city" --model "dall-e-2" --size "1024x1024"

# image to image
uv run python -m examples.hugging-face.image-to-image --image-path "image.png" --prompt "A beautiful sunset over mountains" --model "dall-e-2" --size "1024x1024"

# image to image async
uv run python -m examples.hugging-face.image-to-image-async --image-path "image.png" --prompt "A futuristic city" --model "dall-e-2" --size "1024x1024"


```