import litellm
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from scope3ai.tracers.litellm.chat import (
    litellm_chat_wrapper,
    litellm_async_chat_wrapper,
)


class LiteLLMInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": litellm,
                "name": "completion",
                "wrapper": litellm_chat_wrapper,
            },
            {
                "module": litellm,
                "name": "acompletion",
                "wrapper": litellm_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
