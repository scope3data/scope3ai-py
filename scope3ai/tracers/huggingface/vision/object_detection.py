import io
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, List, Optional, Union

from aiohttp import ClientResponse
from huggingface_hub import (
    AsyncInferenceClient,
    InferenceClient,
    ObjectDetectionOutputElement,
)  # type: ignore[import-untyped]
from PIL import Image
from requests import Response

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.api.typesgen import Image as RootImage
from scope3ai.api.typesgen import Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = PROVIDERS.HUGGINGFACE_HUB.value
HUGGING_FACE_OBJECT_DETECTION_TASK = "object-detection"


@dataclass
class ObjectDetectionOutput:
    elements: Optional[List[ObjectDetectionOutputElement]] = None
    scope3ai: Optional[Scope3AIContext] = None


def _hugging_face_object_detection_get_impact_row(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Optional[Union[ClientResponse, Response]],
    args: Any,
    kwargs: Any,
) -> (ObjectDetectionOutput, ImpactRow):
    compute_time = time.perf_counter() - timer_start
    input_images = []
    if http_response:
        compute_time = http_response.headers.get("x-compute-time") or compute_time
    try:
        image_param = args[0] if len(args) > 0 else kwargs["image"]
        if isinstance(image_param, (str, Path)):
            input_image = Image.open(image_param)
        else:
            input_image = Image.open(io.BytesIO(image_param))
        input_width, input_height = input_image.size
        input_images = [RootImage(root=f"{input_width}x{input_height}")]
    except Exception:
        pass
    scope3_row = ImpactRow(
        model_id=model,
        input_tokens=0,  # No token usage for object detection
        task=Task.object_detection,
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
        input_images=input_images,
    )
    result = ObjectDetectionOutput(elements=response)
    return result, scope3_row


def huggingface_object_detection_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> ObjectDetectionOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_OBJECT_DETECTION_TASK
    )
    result, impact_row = _hugging_face_object_detection_get_impact_row(
        timer_start, model, response, http_response, args, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result


async def huggingface_object_detection_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> ObjectDetectionOutput:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_OBJECT_DETECTION_TASK
    )
    result, impact_row = _hugging_face_object_detection_get_impact_row(
        timer_start, model, response, http_response, args, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result
