import importlib
import io
import logging
import time
from typing import Any, Callable, Optional

import tiktoken
from openai.resources.audio.speech import AsyncSpeech, Speech, _legacy_response

from scope3ai.api.types import ImpactRow, Model, Scope3AIContext, Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI


def _lazy_import(module_name: str, class_name: str):
    def _imported():
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    return _imported


PROVIDER = PROVIDERS.OPENAI.value

MUTAGEN_MAPPING = {
    "mp3": _lazy_import("mutagen.mp3", "MP3"),
    "aac": _lazy_import("mutagen.aac", "AAC"),
    "opus": _lazy_import("mutagen.oggopus", "OggOpus"),
    "flac": _lazy_import("mutagen.flac", "FLAC"),
    "wav": _lazy_import("mutagen.wave", "WAVE"),
}

logger = logging.getLogger(f"scope3ai.tracers.{__name__}")


class HttpxBinaryResponseContent(_legacy_response.HttpxBinaryResponseContent):
    scope3ai: Optional[Scope3AIContext] = None


def _get_audio_duration(format: str, content: bytes) -> Optional[float]:
    try:
        mutagen_cls = MUTAGEN_MAPPING.get(format)
        if mutagen_cls is None:
            logger.error(f"Unsupported audio format: {format}")
            return None
        else:
            mutagen_file = mutagen_cls()(io.BytesIO(content))
            duration = mutagen_file.info.length
    except Exception:
        logger.exception("Failed to estimate audio duration")
        return None

    if format == "wav":
        # bug in mutagen, it returns high number for wav files
        duration = len(content) * 8 / mutagen_file.info.bitrate

    return duration


def _openai_text_to_speech_submit(
    response: _legacy_response.HttpxBinaryResponseContent,
    request_latency: float,
    kwargs: Any,
) -> HttpxBinaryResponseContent:
    # try getting duration
    response_format = kwargs["response_format"]
    duration = _get_audio_duration(response_format, response.content)

    compute_time = response.response.headers.get("openai-processing-ms")
    content_length = response.response.headers.get("content-length")
    if compute_time:
        request_latency = float(compute_time)
    if content_length:
        input_tokens = int(content_length)

    model_requested = kwargs["model"]
    encoder = tiktoken.get_encoding("cl100k_base")
    input_tokens = len(encoder.encode(kwargs["input"]))

    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        input_tokens=input_tokens,
        request_duration_ms=request_latency,
        provider=PROVIDER,
        audio_output_seconds=duration,
        task=Task.text_to_speech,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)

    wrapped_response = HttpxBinaryResponseContent(
        response=response.response,
    )
    wrapped_response.scope3ai = scope3_ctx
    return wrapped_response


def openai_text_to_speech_wrapper(
    wrapped: Callable, instance: Speech, args: Any, kwargs: Any
) -> HttpxBinaryResponseContent:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    return _openai_text_to_speech_submit(response, request_latency, kwargs)


async def openai_async_text_to_speech_wrapper(
    wrapped: Callable, instance: AsyncSpeech, args: Any, kwargs: Any
) -> HttpxBinaryResponseContent:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    return _openai_text_to_speech_submit(response, request_latency, kwargs)
