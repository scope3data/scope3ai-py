import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional, Tuple, Union

from aiohttp import ClientResponse
from huggingface_hub import (
    AsyncInferenceClient,
    InferenceClient,  # type: ignore[import-untyped]
)
from huggingface_hub import (
    AutomaticSpeechRecognitionOutput as _AutomaticSpeechRecognitionOutput,
)
from requests import Response

from scope3ai.api.types import ImpactRow, Scope3AIContext
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


def _hugging_face_automatic_recognition_get_impact_row(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Optional[Union[ClientResponse, Response]],
    args: Any,
    kwargs: Any,
) -> Tuple[AutomaticSpeechRecognitionOutput, ImpactRow]:
    compute_audio_length = None
    compute_time = 0
    if http_response:
        compute_audio_length = http_response.headers.get("x-compute-audio-length")
        compute_time = http_response.headers.get("x-compute-time")
    if not compute_time:
        compute_time = time.perf_counter() - timer_start
    if not compute_audio_length:
        compute_audio_length = 0
    scope3_row = ImpactRow(
        model_id=model,
        task=Task.text_to_speech,
        input_audio_seconds=float(compute_audio_length),
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )
    result = AutomaticSpeechRecognitionOutput(**asdict(response))
    return result, scope3_row


def huggingface_automatic_recognition_output_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_SPEECH_TO_TEXT_TASK
    )
    result, impact_row = _hugging_face_automatic_recognition_get_impact_row(
        timer_start, model, response, http_response, args, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result


async def huggingface_automatic_recognition_output_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_SPEECH_TO_TEXT_TASK
    )
    result, impact_row = _hugging_face_automatic_recognition_get_impact_row(
        timer_start, model, response, http_response, args, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result
