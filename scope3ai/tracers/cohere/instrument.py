from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]
from .chat import (
    cohere_chat_wrapper,
    cohere_async_chat_wrapper,
    cohere_stream_chat_wrapper,
    cohere_async_stream_chat_wrapper,
)


class CohereInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "cohere.base_client",
                "name": "BaseCohere.chat",
                "wrapper": cohere_chat_wrapper,
            },
            {
                "module": "cohere.base_client",
                "name": "AsyncBaseCohere.chat",
                "wrapper": cohere_async_chat_wrapper,
            },
            {
                "module": "cohere.base_client",
                "name": "BaseCohere.chat_stream",
                "wrapper": cohere_stream_chat_wrapper,
            },
            {
                "module": "cohere.base_client",
                "name": "AsyncBaseCohere.chat_stream",
                "wrapper": cohere_async_stream_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
