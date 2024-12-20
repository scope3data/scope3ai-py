import time
import tiktoken
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional, Union

from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from huggingface_hub import (
    AutomaticSpeechRecognitionOutput as _AutomaticSpeechRecognitionOutput,
)
from requests import Response

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI

PROVIDER = "huggingface_hub"


@dataclass
class SpeechToTextOutput(_AutomaticSpeechRecognitionOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_speech_to_text_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> SpeechToTextOutput:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = (time.perf_counter() - timer_start) * 1000
    if kwargs.get("model"):
        model_requested = kwargs.get("model")
        model_used = kwargs.get("model")
    else:
        recommended_model = instance.get_recommended_model(
            "automatic-speech-recognition"
        )
        model_requested = recommended_model
        model_used = recommended_model
    encoder = tiktoken.get_encoding("cl100k_base")
    http_response: Union[Response, None] = getattr(instance, "response")
    input_audio_seconds = 0
    if http_response is not None:
        if http_response.headers.get("x-compute-time"):
            request_latency = float(http_response.headers.get("x-compute-time"))
        if http_response.headers.get("x-compute-audio-length"):
            input_audio_seconds = float(
                http_response.headers.get("x-compute-audio-length")
            )
    output_tokens = len(encoder.encode(response.text))
    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        model_used=Model(id=model_used),
        input_audio_seconds=input_audio_seconds,
        output_tokens=output_tokens,
        task=Task.speech_to_text,
        request_duration_ms=request_latency,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return SpeechToTextOutput(**asdict(response), scope3ai=scope3_ctx)


def huggingface_speech_to_text_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> SpeechToTextOutput:
    return huggingface_speech_to_text_wrapper_non_stream(
        wrapped, instance, args, kwargs
    )
