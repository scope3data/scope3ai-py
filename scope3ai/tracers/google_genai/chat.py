import time
from typing import Any, Callable, Optional
from google.genai.client import Client
from google.genai.types import GenerateContentResponse as _GenerateContentResponse

from scope3ai.api.types import Scope3AIContext
from scope3ai.api.typesgen import ImpactRow
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI

PROVIDER = PROVIDERS.GOOGLE_GENAI.value


class GenerateContentResponse(_GenerateContentResponse):
    scope3ai: Optional[Scope3AIContext] = None


def get_impact_row(response: _GenerateContentResponse, duration_ms: float) -> ImpactRow:
    return ImpactRow(
        model_id=response.model_version,
        input_tokens=response.usage_metadata.prompt_token_count,
        output_tokens=response.usage_metadata.candidates_token_count or 0,
        request_duration_ms=duration_ms * 1000,
    )


def google_genai_chat_wrapper(
    wrapped: Callable, instance: Client, args: Any, kwargs: Any
):
    start = time.time()
    response = wrapped(*args, **kwargs)
    duration_ms = time.time() - start
    impact_row = get_impact_row(response, duration_ms)
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(impact_row)
    response = GenerateContentResponse(**response.to_json_dict())
    response.scope3ai = scope3ai_ctx
    return response


async def google_genai_async_chat_wrapper(
    wrapped: Callable, instance: Client, args: Any, kwargs: Any
):
    start = time.time()
    response = await wrapped(*args, **kwargs)
    duration_ms = time.time() - start
    impact_row = get_impact_row(response, duration_ms)
    scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
    response = GenerateContentResponse(**response.to_json_dict())
    response.scope3ai = scope3ai_ctx
    return response


def google_genai_chat_stream_wrapper(
    wrapped: Callable, instance: Client, args: Any, kwargs: Any
):
    start = time.time()
    stream = wrapped(*args, **kwargs)
    for chunk in stream:
        duration_ms = time.time() - start
        impact_row = get_impact_row(chunk, duration_ms)
        scope3ai_ctx = Scope3AI.get_instance().submit_impact(impact_row)
        chunk = GenerateContentResponse(**chunk.to_json_dict())
        chunk.scope3ai = scope3ai_ctx
        yield chunk


async def google_genai_async_chat_stream_wrapper(
    wrapped: Callable, instance: Client, args: Any, kwargs: Any
):
    start = time.time()
    stream = await wrapped(*args, **kwargs)
    async for chunk in stream:
        duration_ms = time.time() - start
        impact_row = get_impact_row(chunk, duration_ms)
        scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(impact_row)
        chunk = GenerateContentResponse(**chunk.to_json_dict())
        chunk.scope3ai = scope3ai_ctx
        yield chunk
