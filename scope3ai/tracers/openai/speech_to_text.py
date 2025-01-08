import logging
import time
from typing import Any, Callable, Optional, Union

import openai
import tiktoken
from openai.resources.audio.transcriptions import (
    AsyncTranscriptions,
    Transcriptions,
)
from openai.resources.audio.transcriptions import (
    Transcription as _Transcription,
)
from openai.resources.audio.transcriptions import (
    TranscriptionVerbose as _TranscriptionVerbose,
)

from scope3ai.api.types import ImpactRow, Model, Scope3AIContext, Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI

PROVIDER = PROVIDERS.OPENAI.value

logger = logging.getLogger("scope3.tracers.openai.speech_to_text")


class AnnotatedStr(str):
    scope3ai: Optional[Scope3AIContext] = None


class Transcription(_Transcription):
    scope3ai: Optional[Scope3AIContext] = None


class TranscriptionVerbose(_TranscriptionVerbose):
    scope3ai: Optional[Scope3AIContext] = None


def _get_file_audio_duration(
    file: openai._types.FileTypes,
) -> Optional[float]:
    try:
        from mutagen import File

        if isinstance(file, (list, tuple)):
            file = file[1]

        audio = File(file)
        if audio is not None and audio.info is not None:
            return audio.info.length
    except Exception as e:
        logger.exception(f"Failed to get audio duration: {e}")
    return None


def _openai_speech_to_text_wrapper(
    response: Any, request_latency: float, kwargs: dict
) -> Union[Transcription, TranscriptionVerbose, str]:
    model = kwargs["model"]
    encoder = tiktoken.get_encoding("cl100k_base")

    if isinstance(response, (_Transcription, _TranscriptionVerbose)):
        output_tokens = len(encoder.encode(response.text))
    elif isinstance(response, str):
        output_tokens = len(encoder.encode(response))
    else:
        output_tokens = None

    options = {}
    duration = _get_file_audio_duration(kwargs["file"])
    if duration is not None:
        options["input_audio_seconds"] = int(duration)

    scope3_row = ImpactRow(
        model=Model(id=model),
        provider=PROVIDER,
        output_tokens=output_tokens,
        request_duration_ms=request_latency,
        task=Task.speech_to_text,
        **options,
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)

    if isinstance(response, _Transcription):
        result = Transcription.model_construct(**response.model_dump())
    elif isinstance(response, _TranscriptionVerbose):
        result = TranscriptionVerbose.model_construct(**response.model_dump())
    elif isinstance(response, str):
        result = AnnotatedStr(response)
    else:
        logger.error(f"Unexpected response type: {type(response)}")
        return response
    result.scope3ai = scope3_ctx
    return result


def openai_speech_to_text_wrapper(
    wrapped: Callable, instance: Transcriptions, args: Any, kwargs: Any
) -> Union[Transcription, TranscriptionVerbose, str]:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    return _openai_speech_to_text_wrapper(response, request_latency, kwargs)


async def openai_async_speech_to_text_wrapper(
    wrapped: Callable, instance: AsyncTranscriptions, args: Any, kwargs: Any
) -> Union[Transcription, TranscriptionVerbose, str]:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    return _openai_speech_to_text_wrapper(response, request_latency, kwargs)
