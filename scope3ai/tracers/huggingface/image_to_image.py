from dataclasses import dataclass
from typing import Any, Callable, Optional

import tiktoken
from aiohttp import ClientResponse
from huggingface_hub import ImageToImageOutput as _ImageToImageOutput
from huggingface_hub import InferenceClient, AsyncInferenceClient  # type: ignore[import-untyped]
from requests import Response

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = "huggingface_hub"


@dataclass
class ImageToImageOutput(_ImageToImageOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_image_to_image_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> ImageToImageOutput:
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]

    model = kwargs.get("model") or instance.get_recommended_model("text-to-speech")
    compute_time = http_response.headers.get("x-compute-time")
    input_tokens = http_response.headers.get("x-compute-characters")
    # TODO: Load image in memory?
    # input_image = args[0] if len(args) > 0 else kwargs['image']
    # input_width, input_height = input_image.size
    if not input_tokens:
        encoder = tiktoken.get_encoding("cl100k_base")
        prompt = args[1] if len(args) > 1 else kwargs.get("prompt", "")
        input_tokens = len(encoder.encode(prompt)) if prompt != "" else 0
    output_width, output_height = response.size
    scope3_row = ImpactRow(
        model=Model(id=model),
        input_tokens=input_tokens,
        task=Task.image_generation,
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
        output_images=[
            "{width}x{height}".format(width=output_width, height=output_height)
        ],
        # input_images=["{width}x{height}".format(width=input_width, height=input_height)],
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = ImageToImageOutput(response)
    result.scope3ai = scope3_ctx
    return result


async def huggingface_image_to_image_wrapper_async_non_stream(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> ImageToImageOutput:
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model("text-to-speech")
    compute_time = http_response.headers.get("x-compute-time")
    input_tokens = http_response.headers.get("x-compute-characters")
    # TODO: Load image in memory?
    # input_image = args[0] if len(args) > 0 else kwargs['image']
    # input_width, input_height = input_image.size
    if not input_tokens:
        encoder = tiktoken.get_encoding("cl100k_base")
        prompt = args[1] if len(args) > 1 else kwargs.get("prompt", "")
        input_tokens = len(encoder.encode(prompt)) if prompt != "" else 0
    output_width, output_height = response.size
    scope3_row = ImpactRow(
        model=Model(id=model),
        input_tokens=input_tokens,
        task=Task.image_generation,
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
        output_images=[
            "{width}x{height}".format(width=output_width, height=output_height)
        ],
        # input_images=["{width}x{height}".format(width=input_width, height=input_height)],
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = ImageToImageOutput(response)
    result.scope3ai = scope3_ctx
    return result


def huggingface_image_to_image_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> ImageToImageOutput:
    return huggingface_image_to_image_wrapper_non_stream(
        wrapped, instance, args, kwargs
    )


async def huggingface_image_to_image_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> ImageToImageOutput:
    return await huggingface_image_to_image_wrapper_async_non_stream(
        wrapped, instance, args, kwargs
    )
