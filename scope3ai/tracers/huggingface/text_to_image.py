import tiktoken
from dataclasses import dataclass
from typing import Any, Callable, Optional

from huggingface_hub import InferenceClient  # type: ignore[import-untyped]
from huggingface_hub import TextToImageOutput as _TextToImageOutput

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI
from scope3ai.tracers.huggingface.utils import hf_raise_for_status_capture

PROVIDER = "huggingface_hub"


@dataclass
class TextToImageOutput(_TextToImageOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_text_to_image_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TextToImageOutput:
    with hf_raise_for_status_capture() as capture_response:
        response = wrapped(*args, **kwargs)
        http_response = capture_response.get()
    model = kwargs.get("model") or instance.get_recommended_model("text-to-speech")
    encoder = tiktoken.get_encoding("cl100k_base")
    if len(args) > 0:
        prompt = args[0]
    else:
        prompt = kwargs["prompt"]
    compute_time = http_response.headers.get("x-compute-time")
    input_tokens = len(encoder.encode(prompt))
    width, height = response.size
    scope3_row = ImpactRow(
        model=Model(id=model),
        input_tokens=input_tokens,
        task=Task.text_to_image,
        output_images=["{width}x{height}".format(width=width, height=height)],
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return TextToImageOutput(response, scope3ai=scope3_ctx)


def huggingface_text_to_image_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TextToImageOutput:
    return huggingface_text_to_image_wrapper_non_stream(wrapped, instance, args, kwargs)
