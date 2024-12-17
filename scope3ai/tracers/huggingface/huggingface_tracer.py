from scope3ai.tracers.huggingface.chat import (
    huggingface_chat_wrapper,
    huggingface_async_chat_wrapper,
)
from scope3ai.tracers.huggingface.text_to_image import huggingface_text_to_image_wrapper
from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]


class HuggingfaceInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.chat_completion",
                "wrapper": huggingface_chat_wrapper,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.text_to_image",
                "wrapper": huggingface_text_to_image_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.chat_completion",
                "wrapper": huggingface_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
