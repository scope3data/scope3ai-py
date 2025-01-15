import time
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional, Union

from aiohttp import ClientResponse
from huggingface_hub import (
    AutomaticSpeechRecognitionOutput as _AutomaticSpeechRecognitionOutput,
    AsyncInferenceClient,
)
from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from requests import Response

from scope3ai.api.types import Scope3AIContext, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = PROVIDERS.HUGGINGFACE_HUB.value
HUGGING_FACE_SPEECH_TO_TEXT_TASK = "automatic-speech-recognition"


@dataclass
class AutomaticSpeechRecognitionOutput(_AutomaticSpeechRecognitionOutput):
    scope3ai: Optional[Scope3AIContext] = None


def _hugging_face_automatic_recognition_wrapper(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Union[ClientResponse, Response],
    args: Any,
    kwargs: Any,
) -> AutomaticSpeechRecognitionOutput:
    compute_audio_length = None
    if http_response:
        compute_audio_length = http_response.headers.get("x-compute-audio-length")
        compute_time = http_response.headers.get("x-compute-time")
    else:
        compute_time = time.perf_counter() - timer_start
    if not compute_audio_length:
        compute_audio_length = 0
    scope3_row = ImpactRow(
        model=model,
        task=Task.text_to_speech,
        input_audio_seconds=int(float(compute_audio_length)),
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = AutomaticSpeechRecognitionOutput(**asdict(response))
    result.scope3ai = scope3_ctx
    return result


def huggingface_automatic_recognition_output_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_SPEECH_TO_TEXT_TASK
    )
    return _hugging_face_automatic_recognition_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )


async def huggingface_automatic_recognition_output_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_SPEECH_TO_TEXT_TASK
    )
    return _hugging_face_automatic_recognition_wrapper(
        timer_start, model, response, http_response, args, kwargs
    )
