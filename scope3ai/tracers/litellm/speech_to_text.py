import time
from typing import Any, Callable, Optional

import tiktoken
from litellm import Completions
from litellm.types.utils import TranscriptionResponse as _TranscriptionResponse

from scope3ai import Scope3AI
from scope3ai.api.types import ImpactRow
from scope3ai.api.types import Scope3AIContext
from scope3ai.api.typesgen import Task
from scope3ai.constants import PROVIDERS
from scope3ai.tracers.utils.audio import _get_file_audio_duration

PROVIDER = PROVIDERS.LITELLM.value


class TranscriptionResponse(_TranscriptionResponse):
    scope3ai: Optional[Scope3AIContext] = None


def litellm_speech_to_text_get_impact_row(
    timer_start: Any,
    response: TranscriptionResponse,
    args,
    kwargs,
) -> (TranscriptionResponse, ImpactRow):
    request_latency = time.perf_counter() - timer_start
    file = args[0] if len(args) > 0 else kwargs.pop("file")
    model = args[1] if len(args) > 1 else kwargs.pop("model")
    request_latency = getattr(response, "_response_ms", request_latency)
    encoder = tiktoken.get_encoding("cl100k_base")
    options = {}
    duration = _get_file_audio_duration(file)
    if duration is not None:
        options["input_audio_seconds"] = int(duration)
    output_tokens = len(encoder.encode(response.text))
    scope3_row = ImpactRow(
        model_id=model,
        output_tokens=output_tokens,
        request_duration_ms=float(request_latency) * 1000,
        managed_service_id=PROVIDER,
        task=Task.speech_to_text,
        **options,
    )
    return scope3_row


def litellm_speech_to_text_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    keep_tracers = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_tracers) as trace:
        response = wrapped(*args, **kwargs)
        if trace.traces:
            setattr(response, "scope3ai", trace.traces[0])
            return response

    impact_row = litellm_speech_to_text_get_impact_row(
        timer_start, response, args, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response


async def litellm_speech_to_text_wrapper_async(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    keep_tracers = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_tracers) as trace:
        response = await wrapped(*args, **kwargs)
        if trace.traces:
            setattr(response, "scope3ai", trace.traces[0])
            return response
    impact_row = litellm_speech_to_text_get_impact_row(
        timer_start, response, args, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response
