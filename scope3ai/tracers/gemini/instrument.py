from scope3ai.base_tracer import BaseTracer
from scope3ai.tracers.gemini.chat import (
    gemini_async_chat_stream_wrapper,
    gemini_async_chat_wrapper,
    gemini_chat_stream_wrapper,
    gemini_chat_wrapper,
)


class GeminiInstrumentor(BaseTracer):
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "google.genai.models",
                "name": "Models.generate_content",
                "wrapper": gemini_chat_wrapper,
            },
            {
                "module": "google.genai.models",
                "name": "AsyncModels.generate_content",
                "wrapper": gemini_async_chat_wrapper,
            },
            {
                "module": "google.genai.chats",
                "name": "Chat.send_message_stream",
                "wrapper": gemini_chat_stream_wrapper,
            },
            {
                "module": "google.genai.chats",
                "name": "AsyncChat.send_message_stream",
                "wrapper": gemini_async_chat_stream_wrapper,
            },
        ]
