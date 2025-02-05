import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional, Tuple, Union

import tiktoken
from aiohttp import ClientResponse
from huggingface_hub import (  # type: ignore[import-untyped]
    AsyncInferenceClient,
    InferenceClient,
)
from huggingface_hub import TranslationOutput as _TranslationOutput
from requests import Response

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

HUGGING_FACE_TRANSLATION_TASK = "translation"


@dataclass
class TranslationOutput(_TranslationOutput):
    scope3ai: Optional[Scope3AIContext] = None


def _hugging_face_translation_get_impact_row(
    timer_start: Any,
    model: Any,
    response: Any,
    http_response: Optional[Union[ClientResponse, Response]],
    args: Any,
    kwargs: Any,
) -> Tuple[TranslationOutput, ImpactRow]:
    encoder = tiktoken.get_encoding("cl100k_base")
    input_tokens = 0
    compute_time = time.perf_counter() - timer_start
    if http_response:
        compute_time = http_response.headers.get("x-compute-time") or compute_time
        input_tokens = http_response.headers.get("x-compute-characters")
    if not input_tokens:
        prompt = args[0] if len(args) > 0 else kwargs.get("text", "")
        input_tokens = len(encoder.encode(prompt)) if prompt != "" else 0
    output_tokens = len(encoder.encode(response.translation_text))
    scope3_row = ImpactRow(
        model_id=model,
        task=Task.translation,
        input_tokens=int(input_tokens),
        output_tokens=output_tokens,
        request_duration_ms=float(compute_time) * 1000,
    )
    result = TranslationOutput(**asdict(response))
    return result, scope3_row


def huggingface_translation_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TranslationOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_TRANSLATION_TASK
    )
    result, impact_row = _hugging_face_translation_get_impact_row(
        timer_start, model, response, http_response, args, kwargs
    )
    scope3_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result


async def huggingface_translation_wrapper_async_non_stream(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> TranslationOutput:
    timer_start = time.perf_counter()
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model(
        HUGGING_FACE_TRANSLATION_TASK
    )
    result, impact_row = _hugging_face_translation_get_impact_row(
        timer_start, model, response, http_response, args, kwargs
    )
    scope3_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    result.scope3ai = scope3_ctx
    return result
