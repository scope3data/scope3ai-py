import time
from typing import Any, Callable, Optional

from openai.resources.images import AsyncImages, Images
from openai.types.images_response import ImagesResponse as _ImageResponse

from scope3ai.api.types import ImpactRow, Model, Scope3AIContext, Task
from scope3ai.lib import Scope3AI

PROVIDER = "openai"
DEFAULT_MODEL = "dall-e-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_N = 1


class ImageResponse(_ImageResponse):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_image_wrapper(
    response: _ImageResponse, request_latency: float, **kwargs: Any
) -> ImageResponse:
    model = kwargs.get("model", DEFAULT_MODEL)
    size = kwargs.get("size", DEFAULT_SIZE)
    n = kwargs.get("n", DEFAULT_N)

    scope3_row = ImpactRow(
        model=Model(id=model),
        task=Task.text_to_image,
        output_images=[size] * n,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )

    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = ImageResponse.model_construct(**response.model_dump())
    result.scope3ai = scope3ai_ctx
    return result


def openai_image_wrapper(
    wrapped: Callable, instance: Images, args: Any, kwargs: Any
) -> ImageResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    return _openai_image_wrapper(response, request_latency, **kwargs)


async def openai_async_image_wrapper(
    wrapped: Callable, instance: AsyncImages, args: Any, kwargs: Any
) -> ImageResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    return _openai_image_wrapper(response, request_latency, **kwargs)
