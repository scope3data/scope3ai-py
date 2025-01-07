from dataclasses import dataclass, asdict
from typing import Any, Callable, Optional

import tiktoken
from aiohttp import ClientResponse
from huggingface_hub import InferenceClient, AsyncInferenceClient  # type: ignore[import-untyped]
from huggingface_hub import TranslationOutput as _TranslationOutput
from requests import Response

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.api.typesgen import Task
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_response_capture
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = "huggingface_hub"


@dataclass
class TranslationOutput(_TranslationOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_translation_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TranslationOutput:
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model("text-to-speech")
    encoder = tiktoken.get_encoding("cl100k_base")
    if len(args) > 0:
        prompt = args[0]
    else:
        prompt = kwargs["text"]
    compute_time = http_response.headers.get("x-compute-time")
    input_tokens = len(encoder.encode(prompt))
    output_tokens = len(encoder.encode(response.translation_text))
    scope3_row = ImpactRow(
        model=Model(id=model),
        task=Task.translation,
        input_tokens=input_tokens,
        output_tokens=output_tokens,  # TODO: How we can calculate the output tokens of a translation?
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = TranslationOutput(**asdict(response))
    result.scope3ai = scope3_ctx
    return result


async def huggingface_translation_wrapper_async_non_stream(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> TranslationOutput:
    http_response: ClientResponse | None = None
    with aiohttp_response_capture() as responses:
        response = await wrapped(*args, **kwargs)
        http_responses = responses.get()
        if len(http_responses) > 0:
            http_response = http_responses[-1]
    model = kwargs.get("model") or instance.get_recommended_model("text-to-speech")
    encoder = tiktoken.get_encoding("cl100k_base")
    if len(args) > 0:
        prompt = args[0]
    else:
        prompt = kwargs["text"]
    compute_time = http_response.headers.get("x-compute-time")
    input_tokens = len(encoder.encode(prompt))
    output_tokens = len(encoder.encode(response.translation_text))
    scope3_row = ImpactRow(
        model=Model(id=model),
        task=Task.translation,
        input_tokens=input_tokens,
        output_tokens=output_tokens,  # TODO: How we can calculate the output tokens of a translation?
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    result = TranslationOutput(**asdict(response))
    result.scope3ai = scope3_ctx
    return result


async def huggingface_text_to_image_wrapper_async(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> TranslationOutput:
    return huggingface_translation_wrapper_async_non_stream(
        wrapped, instance, args, kwargs
    )


def huggingface_text_to_image_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> TranslationOutput:
    return huggingface_translation_wrapper_non_stream(wrapped, instance, args, kwargs)
