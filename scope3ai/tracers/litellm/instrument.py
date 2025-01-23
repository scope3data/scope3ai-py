import litellm

from scope3ai.base_tracer import BaseTracer
from scope3ai.tracers.litellm.chat import (
    litellm_chat_wrapper,
    litellm_async_chat_wrapper,
)
from scope3ai.tracers.litellm.speech_to_text import (
    litellm_speech_to_text_wrapper,
    litellm_speech_to_text_wrapper_async,
)
from scope3ai.tracers.litellm.text_to_image import (
    litellm_image_generation_wrapper_async,
    litellm_image_generation_wrapper,
)
from scope3ai.tracers.litellm.text_to_speech import (
    litellm_speech_generation_wrapper,
    litellm_speech_generation_wrapper_async,
)


class LiteLLMInstrumentor(BaseTracer):
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
            {
                "module": litellm,
                "name": "image_generation",
                "wrapper": litellm_image_generation_wrapper,
            },
            {
                "module": litellm,
                "name": "aimage_generation",
                "wrapper": litellm_image_generation_wrapper_async,
            },
            {
                "module": litellm,
                "name": "speech",
                "wrapper": litellm_speech_generation_wrapper,
            },
            {
                "module": litellm,
                "name": "aspeech",
                "wrapper": litellm_speech_generation_wrapper_async,
            },
            {
                "module": litellm,
                "name": "transcription",
                "wrapper": litellm_speech_to_text_wrapper,
            },
            {
                "module": litellm,
                "name": "atranscription",
                "wrapper": litellm_speech_to_text_wrapper_async,
            },
        ]
