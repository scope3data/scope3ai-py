import time
from collections.abc import AsyncIterator, Iterator
from typing import Any, Callable, Optional, Union, Literal
from typing_extensions import Annotated

from cohere import ClientV2
from cohere.core.unchecked_base_model import UncheckedBaseModel, UnionMetadata
from cohere.types.chat_response import ChatResponse as _ChatResponse
from cohere.types.streamed_chat_response_v2 import (
    StreamedChatResponseV2 as _StreamedChatResponseV2,
)

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI

PROVIDER = PROVIDERS.COHERE.value


class ChatResponse(_ChatResponse):
    scope3ai: Optional[Scope3AIContext] = None


class Scope3AIStreamedChatResponseV2(UncheckedBaseModel):
    type: Literal["scope3ai"] = "scope3ai"
    scope3ai: Optional[Scope3AIContext] = None


StreamedChatResponseV2 = Annotated[
    Union[
        _StreamedChatResponseV2.__args__[0],
        Scope3AIStreamedChatResponseV2,
    ],
    UnionMetadata(discriminant="type"),
]


def cohere_chat_v2_wrapper(
    wrapped: Callable,
    instance: ClientV2,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> ChatResponse:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = kwargs["model"]
    scope3_row = ImpactRow(
        model_id=model_name,
        input_tokens=response.usage.tokens.input_tokens,
        output_tokens=response.usage.tokens.output_tokens,
        request_duration_ms=request_latency * 1000,
    )
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return ChatResponse(**response.dict(), scope3ai=scope3ai_ctx)


async def cohere_async_chat_v2_wrapper(
    wrapped: Callable,
    instance: ClientV2,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> ChatResponse:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model_name = kwargs["model"]
    scope3_row = ImpactRow(
        model_id=model_name,
        input_tokens=response.usage.tokens.input_tokens,
        output_tokens=response.usage.tokens.output_tokens,
        request_duration_ms=request_latency * 1000,
    )
    scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
    return ChatResponse(**response.dict(), scope3ai=scope3ai_ctx)


def cohere_stream_chat_v2_wrapper(
    wrapped: Callable,
    instance: ClientV2,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> Iterator[StreamedChatResponseV2]:
    model_name = kwargs["model"]
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    for event in stream:
        yield event
        if event.type == "message-end":
            request_latency = time.perf_counter() - timer_start
            input_tokens = event.delta.usage.tokens.input_tokens
            output_tokens = event.delta.usage.tokens.output_tokens
            scope3_row = ImpactRow(
                model_id=model_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                request_duration_ms=request_latency * 1000,
            )
            scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
            yield Scope3AIStreamedChatResponseV2(type="scope3ai", scope3ai=scope3ai_ctx)


async def cohere_async_stream_chat_v2_wrapper(
    wrapped: Callable,
    instance: ClientV2,
    args: Any,
    kwargs: Any,  # noqa: ARG001
) -> AsyncIterator[StreamedChatResponseV2]:
    model_name = kwargs["model"]
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    async for event in stream:
        yield event
        if event.type == "message-end":
            request_latency = time.perf_counter() - timer_start
            input_tokens = event.delta.usage.tokens.input_tokens
            output_tokens = event.delta.usage.tokens.output_tokens
            scope3_row = ImpactRow(
                model_id=model_name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                request_duration_ms=request_latency * 1000,
            )
            scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
            yield Scope3AIStreamedChatResponseV2(type="scope3ai", scope3ai=scope3ai_ctx)
