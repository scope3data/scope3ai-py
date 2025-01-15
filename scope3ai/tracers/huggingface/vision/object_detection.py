import io
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, Union, List

from PIL import Image
from aiohttp import ClientResponse
from huggingface_hub import (
    InferenceClient,
    AsyncInferenceClient,
    ObjectDetectionOutputElement,
)  # type: ignore[import-untyped]
from requests import Response

from scope3ai.api.types import Scope3AIContext, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = PROVIDERS.HUGGINGFACE_HUB.value
HUGGING_FACE_OBJECT_DETECTION_TASK = "object-detection"


@dataclass
class ObjectDetectionOutput:
    elements: List[ObjectDetectionOutputElement] = None
    scope3ai: Optional[Scope3AIContext] = None


def _hugging_face_object_detection_wrapper(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Union[ClientResponse, Response],
    args: Any,
    kwargs: Any,
) -> ObjectDetectionOutput:
    input_tokens = 0
    if http_response:
        compute_time = http_response.headers.get("x-compute-time")
    else:
        compute_time = time.perf_counter() - timer_start
    try:
        image_param = args[0] if len(args) > 0 else kwargs["image"]
        if type(image_param) is str:
            input_image = Image.open(args[0] if len(args) > 0 else kwargs["image"])
        else:
            input_image = Image.open(io.BytesIO(image_param))
        input_width, input_height = input_image.size
        input_images = [
            ("{width}x{height}".format(width=input_width, height=input_height))
        ]
    except Exception:
        pass
    scope3_row = ImpactRow(
        model=model,
        input_tokens=input_tokens,
        task=Task.object_detection,
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
        input_images=input_images,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = ObjectDetectionOutput()
    result.elements = response
    result.scope3ai = scope3_ctx
    return result


def huggingface_object_detection_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> ObjectDetectionOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_OBJECT_DETECTION_TASK
    )
    return _hugging_face_object_detection_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )


async def huggingface_object_detection_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> ObjectDetectionOutput:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_OBJECT_DETECTION_TASK
    )
    return _hugging_face_object_detection_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )
