from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]
from .chat import (
    anthropic_chat_wrapper,
    anthropic_async_chat_wrapper,
    anthropic_stream_chat_wrapper,
    anthropic_async_stream_chat_wrapper,
)


class AnthropicInstrumentor:
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

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
