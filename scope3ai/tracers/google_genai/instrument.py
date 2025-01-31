from scope3ai.base_tracer import BaseTracer
from scope3ai.tracers.google_genai.chat import (
    google_genai_async_chat_stream_wrapper,
    google_genai_async_chat_wrapper,
    google_genai_chat_stream_wrapper,
    google_genai_chat_wrapper,
)


class GoogleGenAiInstrumentor(BaseTracer):
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "google.genai.models",
                "name": "Models.generate_content",
                "wrapper": google_genai_chat_wrapper,
            },
            {
                "module": "google.genai.models",
                "name": "AsyncModels.generate_content",
                "wrapper": google_genai_async_chat_wrapper,
            },
            {
                "module": "google.genai.chats",
                "name": "Chat.send_message_stream",
                "wrapper": google_genai_chat_stream_wrapper,
            },
            {
                "module": "google.genai.chats",
                "name": "AsyncChat.send_message_stream",
                "wrapper": google_genai_async_chat_stream_wrapper,
            },
        ]
