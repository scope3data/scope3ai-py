import time
from typing import Any, Callable, Optional, Tuple

from openai.resources.images import AsyncImages, Images
from openai.types.images_response import ImagesResponse as _ImageResponse
from scope3ai.api.types import ImpactRow, Scope3AIContext, Task
from scope3ai.api.typesgen import Image as RootImage
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.tracers.openai.utils import BaseModelResponse

PROVIDER = PROVIDERS.OPENAI.value
DEFAULT_MODEL = "dall-e-2"
DEFAULT_SIZE = "1024x1024"
DEFAULT_N = 1


class ImageResponse(BaseModelResponse, _ImageResponse):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_image_get_impact_row(
    response: _ImageResponse, request_latency: float, **kwargs: Any
) -> Tuple[ImageResponse, ImpactRow]:
    model = kwargs.get("model", DEFAULT_MODEL)
    size = RootImage(root=kwargs.get("size", DEFAULT_SIZE))
    n = kwargs.get("n", DEFAULT_N)

    scope3_row = ImpactRow(
        model_id=model,
        task=Task.text_to_image,
        output_images=[size] * n,
        request_duration_ms=request_latency * 1000,
    )

    result = ImageResponse.model_construct(**response.model_dump())
    return result, scope3_row


def openai_image_wrapper(
    wrapped: Callable, instance: Images, args: Any, kwargs: Any
) -> ImageResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    result, impact_row = _openai_image_get_impact_row(
        response, request_latency, **kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result


async def openai_async_image_wrapper(
    wrapped: Callable, instance: AsyncImages, args: Any, kwargs: Any
) -> ImageResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    result, impact_row = _openai_image_get_impact_row(
        response, request_latency, **kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result
