import time
from typing import Any, Callable, Optional

import tiktoken
from litellm import Completions
from litellm.utils import ImageResponse as _ImageResponse

from scope3ai import Scope3AI
from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.api.typesgen import Image as RootImage, Task
from scope3ai.constants import PROVIDERS

PROVIDER = PROVIDERS.LITELLM.value
DEFAULT_MODEL = "dall-e-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_N = 1


class ImageResponse(_ImageResponse):
    scope3ai: Optional[Scope3AIContext] = None


def litellm_image_generation_get_impact_row(
    timer_start: Any,
    response: ImageResponse,
    args,
    kwargs,
) -> ImpactRow:
    request_latency = time.perf_counter() - timer_start
    prompt = args[0] if len(args) > 0 else kwargs.get("prompt")
    model = args[1] if len(args) > 1 else kwargs.get("model")
    request_latency = getattr(response, "_response_ms", request_latency)

    encoder = tiktoken.get_encoding("cl100k_base")
    input_tokens = len(encoder.encode(prompt))
    n = kwargs.get("n", DEFAULT_N)
    size = RootImage(root=kwargs.get("size", DEFAULT_SIZE))

    scope3_row = ImpactRow(
        model_id=model or DEFAULT_MODEL,
        task=Task.text_to_image,
        request_duration_ms=float(request_latency) * 1000,
        managed_service_id=PROVIDER,
        output_images=[size] * n,
        input_tokens=input_tokens,
    )
    return scope3_row


def litellm_image_generation_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_traces) as tracer:
        response = wrapped(*args, **kwargs)
        if tracer.traces:
            setattr(response, "scope3ai", tracer.traces[0])
            return response

    impact_row = litellm_image_generation_get_impact_row(
        timer_start, response, args, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response


async def litellm_image_generation_wrapper_async(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
):
    timer_start = time.perf_counter()
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_traces) as tracer:
        response = await wrapped(*args, **kwargs)
        if tracer.traces:
            setattr(response, "scope3ai", tracer.traces[0])
            return response

    impact_row = litellm_image_generation_get_impact_row(
        timer_start, response, args, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    response.scope3ai = scope3_ctx
    return response
