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
                "module": "google.genai",
                "name": "Client.models.generate_content",
                "wrapper": gemini_chat_wrapper,
            },
            {
                "module": "gemini.client",
                "name": "Client.aio.models.generate_content",
                "wrapper": gemini_async_chat_wrapper,
            },
            {
                "module": "gemini.client",
                "name": "Client.chats.send_message_stream",
                "wrapper": gemini_chat_stream_wrapper,
            },
            {
                "module": "gemini.client",
                "name": "Client.aio.chats.send_message_stream",
                "wrapper": gemini_async_chat_stream_wrapper,
            },
        ]
