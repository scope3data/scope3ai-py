from wrapt import wrap_function_wrapper  # type: ignore[import-untyped]

from scope3ai.tracers.huggingface.chat import (
    huggingface_chat_wrapper,
    huggingface_async_chat_wrapper,
)
from scope3ai.tracers.huggingface.image_to_image import (
    huggingface_image_to_image_wrapper,
    huggingface_image_to_image_wrapper_async,
)
from scope3ai.tracers.huggingface.speech_to_text import (
    huggingface_automatic_recognition_output_wrapper,
    huggingface_automatic_recognition_output_wrapper_async,
)
from scope3ai.tracers.huggingface.text_to_image import (
    huggingface_text_to_image_wrapper,
    huggingface_text_to_image_wrapper_async,
)
from scope3ai.tracers.huggingface.text_to_speech import (
    huggingface_text_to_speech_wrapper,
    huggingface_text_to_speech_wrapper_async,
)
from scope3ai.tracers.huggingface.translation import (
    huggingface_translation_wrapper_non_stream,
    huggingface_translation_wrapper_async_non_stream,
)
from scope3ai.tracers.huggingface.vision.image_classification import (
    huggingface_image_classification_wrapper,
    huggingface_image_classification_wrapper_async,
)
from scope3ai.tracers.huggingface.vision.image_segmentation import (
    huggingface_image_segmentation_wrapper,
    huggingface_image_segmentation_wrapper_async,
)
from scope3ai.tracers.huggingface.vision.object_detection import (
    huggingface_object_detection_wrapper,
    huggingface_object_detection_wrapper_async,
)


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
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.translation",
                "wrapper": huggingface_translation_wrapper_async_non_stream,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.text_to_speech",
                "wrapper": huggingface_text_to_speech_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.text_to_speech",
                "wrapper": huggingface_text_to_speech_wrapper_async,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.automatic_speech_recognition",
                "wrapper": huggingface_automatic_recognition_output_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.automatic_speech_recognition",
                "wrapper": huggingface_automatic_recognition_output_wrapper_async,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.chat_completion",
                "wrapper": huggingface_async_chat_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.text_to_image",
                "wrapper": huggingface_text_to_image_wrapper_async,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.image_to_image",
                "wrapper": huggingface_image_to_image_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.image_to_image",
                "wrapper": huggingface_image_to_image_wrapper_async,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.image_classification",
                "wrapper": huggingface_image_classification_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.image_classification",
                "wrapper": huggingface_image_classification_wrapper_async,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.image_segmentation",
                "wrapper": huggingface_image_segmentation_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.image_segmentation",
                "wrapper": huggingface_image_segmentation_wrapper_async,
            },
            {
                "module": "huggingface_hub.inference._client",
                "name": "InferenceClient.object_detection",
                "wrapper": huggingface_object_detection_wrapper,
            },
            {
                "module": "huggingface_hub.inference._generated._async_client",
                "name": "AsyncInferenceClient.object_detection",
                "wrapper": huggingface_object_detection_wrapper_async,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
