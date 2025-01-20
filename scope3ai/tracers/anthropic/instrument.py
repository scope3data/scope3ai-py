from .chat import (
    anthropic_chat_wrapper,
    anthropic_async_chat_wrapper,
    anthropic_stream_chat_wrapper,
    anthropic_async_stream_chat_wrapper,
)
from ...base_tracer import BaseTracer


class AnthropicInstrumentor(BaseTracer):
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "anthropic.resources",
                "name": "Messages.create",
                "wrapper": anthropic_chat_wrapper,
            },
            {
                "module": "anthropic.resources",
                "name": "AsyncMessages.create",
                "wrapper": anthropic_async_chat_wrapper,
            },
            {
                "module": "anthropic.resources",
                "name": "Messages.stream",
                "wrapper": anthropic_stream_chat_wrapper,
            },
            {
                "module": "anthropic.resources",
                "name": "AsyncMessages.stream",
                "wrapper": anthropic_async_stream_chat_wrapper,
            },
        ]
