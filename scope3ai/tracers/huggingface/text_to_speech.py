import time
import tiktoken
from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional

from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from huggingface_hub import TextToSpeechOutput as _TextToSpeechOutput

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI

PROVIDER = "huggingface_hub"


@dataclass
class TextToSpeechOutput(_TextToSpeechOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_text_to_speech_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TextToSpeechOutput:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    if kwargs.get("model"):
        model_requested = kwargs.get("model")
        model_used = kwargs.get("model")
    else:
        recommended_model = instance.get_recommended_model("text-to-speech")
        model_requested = recommended_model
        model_used = recommended_model
    encoder = tiktoken.get_encoding("cl100k_base")
    if len(args) > 0:
        prompt = args[0]
    else:
        prompt = kwargs["text"]
    input_tokens = len(encoder.encode(prompt))
    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        model_used=Model(id=model_used),
        input_tokens=input_tokens,
        task=Task.text_to_speech,
        request_duration_ms=request_latency
        * 1000,  # TODO: can we get the header that has the processing time
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return TextToSpeechOutput(**asdict(response), scope3ai=scope3_ctx)


def huggingface_text_to_speech_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TextToSpeechOutput:
    return huggingface_text_to_speech_wrapper_non_stream(
        wrapped, instance, args, kwargs
    )