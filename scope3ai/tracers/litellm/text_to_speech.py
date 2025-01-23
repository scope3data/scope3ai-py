import time
from typing import Any, Callable, Optional

import tiktoken
from litellm import Completions
from openai.resources.audio.speech import _legacy_response

from scope3ai import Scope3AI
from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.constants import PROVIDERS
from scope3ai.tracers.utils.audio import _get_audio_duration

PROVIDER = PROVIDERS.LITELLM.value


class HttpxBinaryResponseContent(_legacy_response.HttpxBinaryResponseContent):
    scope3ai: Optional[Scope3AIContext] = None


def litellm_speech_generation_get_impact_row(
    timer_start: any,
    response: _legacy_response.HttpxBinaryResponseContent,
    args,
    kwargs,
) -> (HttpxBinaryResponseContent, ImpactRow):
    request_latency = time.perf_counter() - timer_start
    model = args[0] if len(args) > 0 else kwargs.get("model")
    text = args[1] if len(args) > 1 else kwargs.get("input")
    request_latency = getattr(response, "_response_ms", request_latency)

    # Calculate token usage for the input text
    encoder = tiktoken.get_encoding("cl100k_base")
    input_tokens = len(encoder.encode(text))
    response_format = kwargs.get("response_format", "mp3")
    duration = _get_audio_duration(response_format, response.content)
    options = {
        "input_tokens": input_tokens,
    }
    if duration is not None:
        options["output_audio_seconds"] = duration
    scope3_row = ImpactRow(
        model_id=model,
        request_duration_ms=float(request_latency) * 1000,
        managed_service_id=PROVIDER,
        **options,
    )
    return scope3_row


def litellm_speech_generation_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_traces) as tracer:
        response = wrapped(*args, **kwargs)
        if tracer.traces:
            setattr(response, "scope3ai", tracer.traces[0])
            return response

    impact_row = litellm_speech_generation_get_impact_row(
        timer_start, response, args, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response


async def litellm_speech_generation_wrapper_async(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_traces) as tracer:
        response = await wrapped(*args, **kwargs)
        if tracer.traces:
            setattr(response, "scope3ai", tracer.traces[0])
            return response

    impact_row = litellm_speech_generation_get_impact_row(
        timer_start, response, args, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response
