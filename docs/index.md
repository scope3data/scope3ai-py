# 👋 Welcome to Scope3AI Python SDK documentation

Scope3AI is a Python SDK that integrates with popular AI and ML libraries like
OpenAI, Anthropic, HuggingFace, etc. to track, measure, and report on the
environmental impact of AI model usage. It provides an easy interface to the
Scope3AI API for recording interactions and analyzing sustainability metrics
like energy consumption, carbon emissions, and water usage.

## 📖 Documentation

- [Quickstart Guide](quickstart.md) - Get up and running quickly with Scope3AI
- [Working with Tracers](tracer.md) - Learn how to work with tracers to measure AI impact
- [API Reference](api/scope3ai.md) - Detailed API documentation

# Supported libraries

| Library/SDK | Text generation | TTS | STT | Image Generation | Translation | Multimodal input | Multimodal output |
|-------------|-----------------|----|-----|------------------|-----------|------------------|-------------------|
| Anthropic   | ✅              |    |     |                  |           |                  |
| Cohere      | ✅              |    |     |                  |           |                  |
| OpenAI      | ✅              | ✅ | ✅  | ✅               | ✅        | Images/Audio     | Text/Audio
| Huggingface | ✅              | ✅ | ✅  | ✅               | ✅        |                  |
| LiteLLM     | ✅              | ✅ | ✅  | ✅               |           | Images/Audio     | Text/Audio
| MistralAi   | ✅              |    |     |                  |           | Images           |
