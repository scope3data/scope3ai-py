import time
from collections.abc import AsyncIterator, Iterator
from typing import Any, Callable, Optional

from cohere import AsyncClient, Client
from cohere.types.non_streamed_chat_response import (
    NonStreamedChatResponse as _NonStreamedChatResponse,
)
from cohere.types.streamed_chat_response import StreamedChatResponse
from cohere.types.streamed_chat_response import (
    StreamEndStreamedChatResponse as _StreamEndStreamedChatResponse,
)
from scope3ai.lib import Scope3AI
from scope3ai.api.types import Scope3AIContext, Model, ImpactRow

PROVIDER = "cohere"


class NonStreamedChatResponse(_NonStreamedChatResponse):
    scope3ai: Optional[Scope3AIContext] = None

    class Config:
        arbitrary_types_allowed = True


class StreamEndStreamedChatResponse(_StreamEndStreamedChatResponse):
    scope3ai: Optional[Scope3AIContext] = None

    class Config:
        arbitrary_types_allowed = True


def cohere_chat_wrapper(
    wrapped: Callable,
    instance: Client,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> NonStreamedChatResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = kwargs.get("model", "command-r")
    scope3_row = ImpactRow(
        model=Model(id=model_name),
        input_tokens=response.meta.tokens.input_tokens,
        output_tokens=response.meta.tokens.output_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return NonStreamedChatResponse(**response.dict(), scope3ai=scope3ai_ctx)


async def cohere_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncClient,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> NonStreamedChatResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = kwargs.get("model", "command-r")
    scope3_row = ImpactRow(
        model=Model(id=model_name),
        input_tokens=response.meta.tokens.input_tokens,
        output_tokens=response.meta.tokens.output_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return NonStreamedChatResponse(**response.dict(), scope3ai=scope3ai_ctx)


def cohere_stream_chat_wrapper(
    wrapped: Callable,
    instance: Client,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> Iterator[StreamedChatResponse]:
    model_name = kwargs.get("model", "command-r")
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    for event in stream:
        if event.event_type == "stream-end":
            request_latency = time.perf_counter() - timer_start
            input_tokens = event.response.meta.tokens.input_tokens
            output_tokens = event.response.meta.tokens.output_tokens
            scope3_row = ImpactRow(
                model=Model(id=model_name),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                request_duration_ms=request_latency * 1000,
                managed_service_id=PROVIDER,
            )
            scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
            yield StreamEndStreamedChatResponse(**event.dict(), scope3ai=scope3ai_ctx)
        else:
            yield event


async def cohere_async_stream_chat_wrapper(
    wrapped: Callable,
    instance: AsyncClient,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> AsyncIterator[StreamedChatResponse]:
    model_name = kwargs.get("model", "command-r")
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    async for event in stream:
        if event.event_type == "stream-end":
            request_latency = time.perf_counter() - timer_start
            input_tokens = event.response.meta.tokens.input_tokens
            output_tokens = event.response.meta.tokens.output_tokens
            scope3_row = ImpactRow(
                model=Model(id=model_name),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                request_duration_ms=request_latency * 1000,
                managed_service_id=PROVIDER,
            )
            scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
            yield StreamEndStreamedChatResponse(**event.dict(), scope3ai=scope3ai_ctx)
        else:
            yield event
