from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional

from huggingface_hub import (
    AutomaticSpeechRecognitionOutput as _AutomaticSpeechRecognitionOutput,
)
from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from requests import Response

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI
from ...response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = "huggingface_hub"


@dataclass
class AutomaticSpeechRecognitionOutput(_AutomaticSpeechRecognitionOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_automatic_recognition_output_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[0]
    compute_audio_length = http_response.headers.get("x-compute-audio-length")
    compute_time = http_response.headers.get("x-compute-time")
    model = kwargs.get("model") or instance.get_recommended_model("text-to-speech")

    scope3_row = ImpactRow(
        model=Model(id=model),
        task=Task.text_to_speech,
        output_audio_seconds=int(float(compute_audio_length)),
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
    return huggingface_automatic_recognition_output_wrapper_non_stream(
        wrapped, instance, args, kwargs
    )
