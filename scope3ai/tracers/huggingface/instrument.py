from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from scope3ai.tracers.huggingface.chat import (
    huggingface_chat_wrapper,
    huggingface_async_chat_wrapper,
)
from scope3ai.tracers.huggingface.post_request_interceptor import (
    post_request_interceptor,
)
from scope3ai.tracers.huggingface.speech_to_text import (
    huggingface_speech_to_text_wrapper,
)
from scope3ai.tracers.huggingface.text_to_image import huggingface_text_to_image_wrapper
from scope3ai.tracers.huggingface.text_to_speech import (
    huggingface_text_to_speech_wrapper,
)
from scope3ai.tracers.huggingface.translation import (
    huggingface_translation_wrapper_non_stream,
)


class HuggingfaceInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.post",
                "wrapper": post_request_interceptor,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.chat_completion",
                "wrapper": huggingface_chat_wrapper,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.automatic_speech_recognition",
                "wrapper": huggingface_speech_to_text_wrapper,
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
        for wrapper in self.wrapped_methods:
            # print(wrapper)
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
