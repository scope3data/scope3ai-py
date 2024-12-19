from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from scope3ai.tracers.huggingface.chat import (
    huggingface_chat_wrapper,
    huggingface_async_chat_wrapper,
)
from scope3ai.tracers.huggingface.text_to_image import huggingface_text_to_image_wrapper
from scope3ai.tracers.huggingface.text_to_speech import (
    huggingface_text_to_speech_wrapper,
)
from scope3ai.tracers.huggingface.translation import (
    huggingface_translation_wrapper_non_stream,
)


def my_wrapper(wrapped, instance, args, kwargs):
    # Custom logic before calling the original function
    print("Mocked hf_raise_for_status is called")

    # Optionally, you can call the original function or skip it
    # Uncomment the line below to call the original function
    # return wrapped(*args, **kwargs)

    # Custom mock response
    return "Mocked response"


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
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.translation",
                "wrapper": huggingface_translation_wrapper_non_stream,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.text_to_speech",
                "wrapper": huggingface_text_to_speech_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.chat_completion",
                "wrapper": huggingface_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        wrap_function_wrapper(
            "huggingface_hub.utils",  # Module where the function resides
            "hf_raise_for_status",  # Name of the function to mock
            my_wrapper,  # Your custom wrapper
        )
        for wrapper in self.wrapped_methods:
            # print(wrapper)
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
