from scope3ai.base_tracer import BaseTracer
from .chat import openai_chat_wrapper, openai_async_chat_wrapper
from .speech_to_text import (
    openai_async_speech_to_text_wrapper,
    openai_speech_to_text_wrapper,
)
from .text_to_image import (
    openai_image_wrapper,
    openai_async_image_wrapper,
)
from .text_to_speech import (
    openai_text_to_speech_wrapper,
    openai_async_text_to_speech_wrapper,
)
from .translation import (
    openai_translation_wrapper,
    openai_async_translation_wrapper,
)


class OpenAIInstrumentor(BaseTracer):
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
            {
                "module": "openai.resources.audio.speech",
                "name": "Speech.create",
                "wrapper": openai_text_to_speech_wrapper,
            },
            {
                "module": "openai.resources.audio.speech",
                "name": "AsyncSpeech.create",
                "wrapper": openai_async_text_to_speech_wrapper,
            },
            {
                "module": "openai.resources.audio.transcriptions",
                "name": "Transcriptions.create",
                "wrapper": openai_speech_to_text_wrapper,
            },
            {
                "module": "openai.resources.audio.transcriptions",
                "name": "AsyncTranscriptions.create",
                "wrapper": openai_async_speech_to_text_wrapper,
            },
            {
                "module": "openai.resources.audio.translations",
                "name": "Translations.create",
                "wrapper": openai_translation_wrapper,
            },
            {
                "module": "openai.resources.audio.translations",
                "name": "AsyncTranslations.create",
                "wrapper": openai_async_translation_wrapper,
            },
            {
                "module": "openai.resources.images",
                "name": "Images.create_variation",
                "wrapper": openai_image_wrapper,
            },
            {
                "module": "openai.resources.images",
                "name": "Images.edit",
                "wrapper": openai_image_wrapper,
            },
            {
                "module": "openai.resources.images",
                "name": "Images.generate",
                "wrapper": openai_image_wrapper,
            },
            {
                "module": "openai.resources.images",
                "name": "AsyncImages.create_variation",
                "wrapper": openai_async_image_wrapper,
            },
            {
                "module": "openai.resources.images",
                "name": "AsyncImages.edit",
                "wrapper": openai_async_image_wrapper,
            },
            {
                "module": "openai.resources.images",
                "name": "AsyncImages.generate",
                "wrapper": openai_async_image_wrapper,
            },
        ]
