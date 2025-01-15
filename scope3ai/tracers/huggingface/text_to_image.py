import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

import tiktoken
from aiohttp import ClientResponse
from huggingface_hub import InferenceClient, AsyncInferenceClient  # type: ignore[import-untyped]
from huggingface_hub import TextToImageOutput as _TextToImageOutput
from requests import Response

from scope3ai.api.types import Scope3AIContext, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = PROVIDERS.HUGGINGFACE_HUB.value
HUGGING_FACE_TEXT_TO_IMAGE_TASK = "text-to-image"


@dataclass
class TextToImageOutput(_TextToImageOutput):
    scope3ai: Optional[Scope3AIContext] = None


def _hugging_face_text_to_image_wrapper(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Union[ClientResponse, Response],
    args: Any,
    kwargs: Any,
) -> TextToImageOutput:
    input_tokens = None
    if http_response:
        compute_time = http_response.headers.get("x-compute-time")
        input_tokens = http_response.headers.get("x-compute-characters")
    else:
        compute_time = time.perf_counter() - timer_start
    if not input_tokens:
        encoder = tiktoken.get_encoding("cl100k_base")
        prompt = args[0] if len(args) > 0 else kwargs.get("prompt", "")
        input_tokens = len(encoder.encode(prompt)) if prompt != "" else 0
    width, height = response.size
    scope3_row = ImpactRow(
        model=model,
        input_tokens=input_tokens,
        task=Task.text_to_image,
        output_images=["{width}x{height}".format(width=width, height=height)],
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = TextToImageOutput(response)
    result.scope3ai = scope3_ctx
    return result


def huggingface_text_to_image_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TextToImageOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_TEXT_TO_IMAGE_TASK
    )
    return _hugging_face_text_to_image_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )


async def huggingface_text_to_image_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> TextToImageOutput:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_TEXT_TO_IMAGE_TASK
    )
    return _hugging_face_text_to_image_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )
