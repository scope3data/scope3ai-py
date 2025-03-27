import logging
import time
from typing import Any, Callable, Optional, Union

from litellm import AsyncCompletions, Completions
from litellm.types.utils import ModelResponse
from litellm.utils import CustomStreamWrapper
import tiktoken

from scope3ai import Scope3AI
from scope3ai.api.types import Scope3AIContext, ImpactRow
from scope3ai.constants import CLIENTS, try_provider_for_client
from scope3ai.tracers.utils.multimodal import (
    aggregate_multimodal,
    aggregate_multimodal_audio_content_output,
)


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
    token_count = 0
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_traces):
        stream = wrapped(*args, **kwargs)
    for i, chunk in enumerate(stream):
        if i > 0:
            token_count += 1
        if chunk.choices[0].finish_reason is None:
            yield chunk
            continue
        request_latency = time.perf_counter() - timer_start
        model = args[0] if len(args) > 0 else kwargs.get("model")
        messages = args[1] if len(args) > 1 else kwargs.get("messages")
        prompt = " ".join([message.get("content") for message in messages])
        encoder = tiktoken.get_encoding("cl100k_base")
        input_tokens = len(encoder.encode(prompt))
        if model is None:
            model = chunk.model
        scope3_row = ImpactRow(
            managed_service_id=try_provider_for_client(CLIENTS.LITELLM),
            model_id=model,
            input_tokens=input_tokens,
            output_tokens=token_count,
            request_duration_ms=float(request_latency) * 1000,
        )
        scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        yield ChatCompletionChunk(**chunk.model_dump(), scope3ai=scope3ai_ctx)


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
    model = args[0] if len(args) > 0 else kwargs.get("model")
    if model is None:
        model = response.model
    scope3_row = ImpactRow(
        managed_service_id=try_provider_for_client(CLIENTS.LITELLM),
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
    model = args[0] if len(args) > 0 else kwargs.get("model")
    if model is None:
        model = response.model
    scope3_row = ImpactRow(
        managed_service_id=try_provider_for_client(CLIENTS.LITELLM),
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
    keep_traces = not kwargs.pop("use_always_litellm_tracer", False)
    with Scope3AI.get_instance().trace(keep_traces=keep_traces):
        stream = await wrapped(*args, **kwargs)
    i = 0
    token_count = 0
    async for chunk in stream:
        if i > 0:
            token_count += 1
        if chunk.choices[0].finish_reason is None:
            i += 1
            yield chunk
            continue
        request_latency = time.perf_counter() - timer_start
        model = args[0] if len(args) > 0 else kwargs.get("model")
        messages = args[1] if len(args) > 1 else kwargs.get("messages")
        prompt = " ".join([message.get("content") for message in messages])
        encoder = tiktoken.get_encoding("cl100k_base")
        input_tokens = len(encoder.encode(prompt))
        if model is None:
            model = chunk.model
        scope3_row = ImpactRow(
            managed_service_id=try_provider_for_client(CLIENTS.LITELLM),
            model_id=model,
            input_tokens=input_tokens,
            output_tokens=token_count,
            request_duration_ms=float(request_latency) * 1000,
        )
        scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
        yield ChatCompletionChunk(**chunk.model_dump(), scope3ai=scope3ai_ctx)
