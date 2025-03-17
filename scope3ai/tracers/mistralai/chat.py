import logging
import time
from collections.abc import AsyncGenerator, Iterable
from typing import Any, Callable, Optional

from mistralai import Mistral
from mistralai.models import ChatCompletionResponse as _ChatCompletionResponse
from mistralai.models import CompletionChunk as _CompletionChunk
from mistralai.models import CompletionEvent

from scope3ai import Scope3AI
from scope3ai.api.types import Scope3AIContext
from scope3ai.api.typesgen import ImpactRow
from scope3ai.constants import CLIENTS, try_provider_for_client
from scope3ai.tracers.utils.multimodal import aggregate_multimodal


logger = logging.getLogger("scope3ai.tracers.mistralai.chat")


class ChatCompletionResponse(_ChatCompletionResponse):
    scope3ai: Optional[Scope3AIContext] = None


class CompletionChunk(_CompletionChunk):
    scope3ai: Optional[Scope3AIContext] = None


def mistralai_v1_chat_wrapper(
    wrapped: Callable,
    instance: Mistral,
    args: Any,
    kwargs: Any,
) -> ChatCompletionResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    scope3_row = ImpactRow(
        managed_service_id=try_provider_for_client(CLIENTS.MISTRALAI),
        model_id=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency * 1000,
    )
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    messages = args[1] if len(args) > 1 else kwargs.get("messages")
    for message in messages:
        aggregate_multimodal(message, scope3_row, logger)
    chat = ChatCompletionResponse(**response.model_dump())
    chat.scope3ai = scope3ai_ctx
    return chat


def mistralai_v1_chat_wrapper_stream(
    wrapped: Callable,
    instance: Mistral,
    args: Any,
    kwargs: Any,
) -> Iterable[CompletionEvent]:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    for i, chunk in enumerate(stream):
        model_name = chunk.data.model
        # Mistral returns the full usage in the last chunk only we don't want to submit the impact for the empty chunks
        if not chunk.data or not chunk.data.usage:
            continue
        request_latency = time.perf_counter() - timer_start
        scope3_row = ImpactRow(
            managed_service_id=try_provider_for_client(CLIENTS.MISTRALAI),
            model_id=model_name,
            input_tokens=chunk.data.usage.prompt_tokens,
            output_tokens=chunk.data.usage.completion_tokens,
            request_duration_ms=request_latency * 1000,
        )
        scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        chunk.data = CompletionChunk(**chunk.data.model_dump(), scope3ai=scope3ai_ctx)
        yield chunk


async def mistralai_v1_async_chat_wrapper(
    wrapped: Callable,
    instance: Mistral,
    args: Any,
    kwargs: Any,
) -> ChatCompletionResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    scope3_row = ImpactRow(
        managed_service_id=try_provider_for_client(CLIENTS.MISTRALAI),
        model_id=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency * 1000,
    )
    scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
    chat = ChatCompletionResponse(**response.model_dump())
    chat.scope3ai = scope3ai_ctx
    return chat


async def _generator(
    stream: AsyncGenerator[CompletionEvent, None], timer_start: float
) -> AsyncGenerator[CompletionEvent, None]:
    async for chunk in stream:
        # Mistral returns the full usage in the last chunk only we don't want to submit the impact for the empty chunks
        if not chunk.data or not chunk.data.usage:
            continue
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.data.model
        scope3_row = ImpactRow(
            managed_service_id=try_provider_for_client(CLIENTS.MISTRALAI),
            model_id=model_name,
            input_tokens=chunk.data.usage.prompt_tokens,
            output_tokens=chunk.data.usage.completion_tokens,
            request_duration_ms=request_latency * 1000,
        )
        scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
        chunk.data = CompletionChunk(**chunk.data.model_dump(), scope3ai=scope3ai_ctx)
        yield chunk


async def mistralai_v1_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: Mistral,
    args: Any,
    kwargs: Any,
) -> AsyncGenerator[CompletionEvent, None]:
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    return _generator(stream, timer_start)
