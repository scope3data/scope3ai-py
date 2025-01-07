from wrapt import wrap_function_wrapper

from .chat import openai_chat_wrapper, openai_async_chat_wrapper
from .text_to_speech import (
    openai_text_to_speech_wrapper,
    openai_async_text_to_speech_wrapper,
)
from .speech_to_text import (
    openai_async_speech_to_text_wrapper,
    openai_speech_to_text_wrapper,
)


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
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
