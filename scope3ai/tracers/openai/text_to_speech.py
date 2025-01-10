import logging
import time
from typing import Any, Callable, Optional

import tiktoken
from openai.resources.audio.speech import AsyncSpeech, Speech, _legacy_response

from scope3ai.api.types import ImpactRow, Model, Scope3AIContext, Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI

from .utils import _get_audio_duration

PROVIDER = PROVIDERS.OPENAI.value

logger = logging.getLogger(f"scope3ai.tracers.{__name__}")


class HttpxBinaryResponseContent(_legacy_response.HttpxBinaryResponseContent):
    scope3ai: Optional[Scope3AIContext] = None


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
