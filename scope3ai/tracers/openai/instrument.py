from wrapt import wrap_function_wrapper

from scope3ai.tracers.openai.chat import openai_chat_wrapper, openai_async_chat_wrapper


class OpenAIInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "openai.resources.chat.completions",
                "name": "Completions.create",
                "wrapper": openai_chat_wrapper,
            },
            {
                "module": "openai.resources.chat.completions",
                "name": "AsyncCompletions.create",
                "wrapper": openai_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
