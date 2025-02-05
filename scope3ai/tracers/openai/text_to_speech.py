import logging
import time
from typing import Any, Callable, Optional, Tuple

import tiktoken
from openai.resources.audio.speech import AsyncSpeech, Speech, _legacy_response

from scope3ai.api.types import ImpactRow, Scope3AIContext, Task
from scope3ai.lib import Scope3AI
from scope3ai.tracers.openai.utils import BaseModelResponse
from scope3ai.tracers.utils.audio import _get_audio_duration

logger = logging.getLogger(f"scope3ai.tracers.{__name__}")


class HttpxBinaryResponseContent(
    BaseModelResponse, _legacy_response.HttpxBinaryResponseContent
):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_text_to_speech_get_impact_row(
    response: _legacy_response.HttpxBinaryResponseContent,
    request_latency: float,
    kwargs: Any,
) -> Tuple[HttpxBinaryResponseContent, ImpactRow]:
    # try getting duration
    response_format = kwargs.get("response_format", "mp3")
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
        model_id=model_requested,
        input_tokens=input_tokens,
        request_duration_ms=request_latency,
        output_audio_seconds=duration,
        task=Task.text_to_speech,
    )

    wrapped_response = HttpxBinaryResponseContent(
        response=response.response,
    )
    return wrapped_response, scope3_row


def openai_text_to_speech_wrapper(
    wrapped: Callable, instance: Speech, args: Any, kwargs: Any
) -> HttpxBinaryResponseContent:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    result, impact_row = _openai_text_to_speech_get_impact_row(
        response, request_latency, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result


async def openai_async_text_to_speech_wrapper(
    wrapped: Callable, instance: AsyncSpeech, args: Any, kwargs: Any
) -> HttpxBinaryResponseContent:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    result, impact_row = _openai_text_to_speech_get_impact_row(
        response, request_latency, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result
