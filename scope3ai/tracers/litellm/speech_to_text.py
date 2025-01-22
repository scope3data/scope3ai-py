import time
from typing import Any, Callable, Optional

from litellm import Completions
from litellm.types.utils import TranscriptionResponse as _TranscriptionResponse

from scope3ai import Scope3AI
from scope3ai.api.types import ImpactRow
from scope3ai.api.types import Scope3AIContext
from scope3ai.constants import PROVIDERS

PROVIDER = PROVIDERS.LITELLM.value


class TranscriptionResponse(_TranscriptionResponse):
    scope3ai: Optional[Scope3AIContext] = None


def litellm_speech_to_text_get_impact_row(
    timer_start: Any,
    model,
    response: TranscriptionResponse,
) -> (TranscriptionResponse, ImpactRow):
    request_latency = time.perf_counter() - timer_start
    scope3_row = ImpactRow(
        model_id=model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.total_tokens,
        request_duration_ms=float(request_latency) * 1000,
        managed_service_id=PROVIDER,
    )
    return scope3_row


def litellm_speech_to_text_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    with Scope3AI.get_instance().trace(keep_traces=True) as trace:
        response = wrapped(*args, **kwargs)
        if trace.traces:
            setattr(response, "scope3ai", trace.traces[0])
            return response
    model = args[1] if len(args) > 1 else kwargs.pop("model")
    impact_row = litellm_speech_to_text_get_impact_row(timer_start, response, model)
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response


async def litellm_speech_to_text_wrapper_async(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    with Scope3AI.get_instance().trace(keep_traces=True) as trace:
        response = await wrapped(*args, **kwargs)
        if trace.traces:
            setattr(response, "scope3ai", trace.traces[0])
            return response
    model = args[1] if len(args) > 1 else kwargs.pop("model")
    impact_row = litellm_speech_to_text_get_impact_row(timer_start, response, model)
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response
