from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from scope3ai.tracers.mistrarlai_v1.chat import (
    mistralai_v1_chat_wrapper,
    mistralai_v1_async_chat_wrapper,
    mistralai_v1_chat_wrapper_stream,
    mistralai_v1_async_chat_wrapper_stream,
)


class MistralAIInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "mistralai.chat",
                "name": "Chat.complete",
                "wrapper": mistralai_v1_chat_wrapper,
            },
            {
                "module": "mistralai.chat",
                "name": "Chat.complete_async",
                "wrapper": mistralai_v1_async_chat_wrapper,
            },
            {
                "module": "mistralai.chat",
                "name": "Chat.stream",
                "wrapper": mistralai_v1_chat_wrapper_stream,
            },
            {
                "module": "mistralai.chat",
                "name": "Chat.stream_async",
                "wrapper": mistralai_v1_async_chat_wrapper_stream,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
