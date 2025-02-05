import logging
import time
from typing import Any, Callable, Optional, Union

from litellm import AsyncCompletions, Completions
from litellm.types.utils import ModelResponse
from litellm.utils import CustomStreamWrapper

from scope3ai import Scope3AI
from scope3ai.api.types import Scope3AIContext, ImpactRow
from scope3ai.constants import PROVIDERS
from scope3ai.tracers.utils.multimodal import (
    aggregate_multimodal,
    aggregate_multimodal_audio_content_output,
)

PROVIDER = PROVIDERS.LITELLM.value

logger = logging.getLogger("scope3ai.tracers.litellm.chat")


class ChatCompletion(ModelResponse):
    scope3ai: Optional[Scope3AIContext] = None


class ChatCompletionChunk(ModelResponse):
    scope3ai: Optional[Scope3AIContext] = None


def litellm_chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
) -> Union[ChatCompletion, CustomStreamWrapper]:
    if kwargs.get("stream", False):
        return litellm_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return litellm_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def litellm_chat_wrapper_stream(  # type: ignore[misc]
    wrapped: Callable,
    instance: Completions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> CustomStreamWrapper:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    for i, chunk in enumerate(stream):
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start

        model = chunk.model
        if model is not None:
            scope3_row = ImpactRow(
                model_id=model,
                output_tokens=token_count,
                request_duration_ms=float(request_latency) * 1000,
            )
            scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
            if scope3ai_ctx is not None:
                yield ChatCompletionChunk(**chunk.model_dump(), scope3ai=scope3ai_ctx)
            else:
                yield chunk
        else:
            yield chunk


def litellm_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: Completions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
    timer_start = time.perf_counter()
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    modalities = kwargs.get("modalities", [])
    with Scope3AI.get_instance().trace(keep_traces=keep_traces) as tracer:
        response = wrapped(*args, **kwargs)
        if tracer.traces:
            setattr(response, "scope3ai", tracer.traces[0])
            return response
    request_latency = time.perf_counter() - timer_start
    model = response.model
    if model is None:
        return response
    scope3_row = ImpactRow(
        model_id=model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.total_tokens,
        request_duration_ms=float(request_latency) * 1000,
    )
    if "audio" in modalities:
        audio_format = kwargs.get("audio", {}).get("format", "mp3")
        for choice in response.choices:
            audio_data = getattr(choice.message, "audio")
            if audio_data:
                audio_content = audio_data.data
                aggregate_multimodal_audio_content_output(
                    audio_content, audio_format, scope3_row
                )
    messages = args[1] if len(args) > 1 else kwargs.get("messages")
    for message in messages:
        aggregate_multimodal(message, scope3_row, logger)
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    if scope3ai_ctx is not None:
        return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)
    else:
        return response


async def litellm_async_chat_wrapper(
    wrapped: Callable, instance: AsyncCompletions, args: Any, kwargs: Any
) -> Union[ChatCompletion, CustomStreamWrapper]:
    if kwargs.get("stream", False):
        return litellm_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await litellm_async_chat_wrapper_base(wrapped, instance, args, kwargs)


async def litellm_async_chat_wrapper_base(
    wrapped: Callable,
    instance: AsyncCompletions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
    timer_start = time.perf_counter()
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    modalities = kwargs.get("modalities", [])
    with Scope3AI.get_instance().trace(keep_traces=keep_traces) as tracer:
        response = await wrapped(*args, **kwargs)
        if tracer.traces:
            setattr(response, "scope3ai", tracer.traces[0])
            return response
    request_latency = time.perf_counter() - timer_start
    model = response.model
    if model is None:
        return response
    scope3_row = ImpactRow(
        model_id=model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.total_tokens,
        request_duration_ms=float(request_latency) * 1000,
    )
    if "audio" in modalities:
        audio_format = kwargs.get("audio", {}).get("format", "mp3")
        for choice in response.choices:
            audio_data = getattr(choice.message, "audio")
            if audio_data:
                audio_content = audio_data.data
                aggregate_multimodal_audio_content_output(
                    audio_content, audio_format, scope3_row
                )
    messages = args[1] if len(args) > 1 else kwargs.get("messages")
    for message in messages:
        aggregate_multimodal(message, scope3_row, logger)
    scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
    if scope3ai_ctx is not None:
        return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)
    else:
        return response


async def litellm_async_chat_wrapper_stream(  # type: ignore[misc]
    wrapped: Callable,
    instance: AsyncCompletions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> CustomStreamWrapper:
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    i = 0
    token_count = 0
    async for chunk in stream:
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start
        model = chunk.model
        if model is not None:
            scope3_row = ImpactRow(
                model_id=model,
                output_tokens=token_count,
                request_duration_ms=float(request_latency) * 1000,
            )
            scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
            if scope3ai_ctx is not None:
                yield ChatCompletionChunk(**chunk.model_dump(), scope3ai=scope3ai_ctx)
            else:
                yield chunk
        else:
            yield chunk
        i += 1
