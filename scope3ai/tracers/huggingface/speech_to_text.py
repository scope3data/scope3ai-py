from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional

from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from huggingface_hub import (
    AutomaticSpeechRecognitionOutput as _AutomaticSpeechRecognitionOutput,
)

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI
from .utils import hf_raise_for_status_capture

PROVIDER = "huggingface_hub"


@dataclass
class AutomaticSpeechRecognitionOutput(_AutomaticSpeechRecognitionOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_automatic_recognition_output_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    with hf_raise_for_status_capture() as capture_response:
        response = wrapped(*args, **kwargs)
        http_response = capture_response.get()

    compute_audio_length = http_response.headers.get("x-compute-audio-length")
    compute_time = http_response.headers.get("x-compute-time")
    if kwargs.get("model"):
        model_requested = kwargs.get("model")
        model_used = kwargs.get("model")
    else:
        recommended_model = instance.get_recommended_model(
            "automatic-speech-recognition"
        )
        model_requested = recommended_model
        model_used = recommended_model

    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        model_used=Model(id=model_used),
        task=Task.text_to_speech,
        output_audio_seconds=int(float(compute_audio_length)),
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return AutomaticSpeechRecognitionOutput(**asdict(response), scope3ai=scope3_ctx)


def huggingface_automatic_recognition_output_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> AutomaticSpeechRecognitionOutput:
    return huggingface_automatic_recognition_output_wrapper_non_stream(
        wrapped, instance, args, kwargs
    )
