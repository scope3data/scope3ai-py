import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union

import tiktoken
from aiohttp import ClientResponse
from huggingface_hub import InferenceClient, AsyncInferenceClient  # type: ignore[import-untyped]
from huggingface_hub import (
    ImageClassificationOutputElement as _ImageClassificationOutputElement,
)
from requests import Response

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = PROVIDERS.HUGGINGFACE_HUB.value
HUGGING_FACE_IMAGE_CLASSIFICATION_TASK = "image-classification"


@dataclass
class ImageClassificationOutputElement(_ImageClassificationOutputElement):
    scope3ai: Optional[Scope3AIContext] = None


def _hugging_face_image_classification_wrapper(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Union[ClientResponse, Response],
    args: Any,
    kwargs: Any,
) -> ImageClassificationOutputElement:
    input_tokens = None
    if http_response:
        compute_time = http_response.headers.get("x-compute-time")
        input_tokens = http_response.headers.get("x-compute-characters")
    else:
        compute_time = time.perf_counter() - timer_start
    if not input_tokens:
        encoder = tiktoken.get_encoding("cl100k_base")
        input_data = args[0] if len(args) > 0 else kwargs.get("inputs", "")
        input_tokens = len(encoder.encode(input_data)) if input_data != "" else 0

    scope3_row = ImpactRow(
        model=Model(id=model),
        input_tokens=input_tokens,
        task=Task.image_classification,
        output_images=[],  # No images to output in classification
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = ImageClassificationOutputElement(response)
    result.scope3ai = scope3_ctx
    return result


def huggingface_image_classification_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> ImageClassificationOutputElement:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_IMAGE_CLASSIFICATION_TASK
    )
    return _hugging_face_image_classification_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )


async def huggingface_image_classification_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> ImageClassificationOutputElement:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_IMAGE_CLASSIFICATION_TASK
    )
    return _hugging_face_image_classification_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )
