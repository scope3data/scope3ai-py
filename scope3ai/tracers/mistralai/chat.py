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
from scope3ai.constants import PROVIDERS
from scope3ai.tracers.utils.multimodal import aggregate_multimodal

PROVIDER = PROVIDERS.MISTRALAI.value

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
        model_id=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
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
    token_count = 0
    for i, chunk in enumerate(stream):
        if i > 0 and chunk.data.choices[0].finish_reason is None:
            token_count += 1
        model_name = chunk.data.model
        if chunk.data:
            request_latency = time.perf_counter() - timer_start
            scope3_row = ImpactRow(
                model_id=model_name,
                input_tokens=token_count,
                output_tokens=chunk.data.usage.completion_tokens
                if chunk.data.usage
                else 0,
                request_duration_ms=request_latency * 1000,
                managed_service_id=PROVIDER,
            )
            scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
            chunk.data = CompletionChunk(
                **chunk.data.model_dump(), scope3ai=scope3ai_ctx
            )
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
        model_id=response.model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )
    scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
    chat = ChatCompletionResponse(**response.model_dump())
    chat.scope3ai = scope3ai_ctx
    return chat


async def _generator(
    stream: AsyncGenerator[CompletionEvent, None], timer_start: float
) -> AsyncGenerator[CompletionEvent, None]:
    token_count = 0
    async for chunk in stream:
        if chunk.data.usage is not None:
            token_count = chunk.data.usage.completion_tokens
        request_latency = time.perf_counter() - timer_start
        model_name = chunk.data.model
        scope3_row = ImpactRow(
            model_id=model_name,
            input_tokens=token_count,
            output_tokens=chunk.data.usage.completion_tokens if chunk.data.usage else 0,
            request_duration_ms=request_latency * 1000,
            managed_service_id=PROVIDER,
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
