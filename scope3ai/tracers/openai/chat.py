import logging
import time
from typing import Any, Callable, Optional, Union

from openai import AsyncStream, Stream
from openai._legacy_response import LegacyAPIResponse
from openai.resources.chat import AsyncCompletions, Completions
from openai.types.chat import ChatCompletion as _ChatCompletion
from openai.types.chat import ChatCompletionChunk as _ChatCompletionChunk

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.tracers.utils.multimodal import aggregate_multimodal

PROVIDER = PROVIDERS.OPENAI.value

logger = logging.getLogger("scope3ai.tracers.openai.chat")


class ChatCompletion(_ChatCompletion):
    scope3ai: Optional[Scope3AIContext] = None


class ChatCompletionChunk(_ChatCompletionChunk):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_chat_wrapper(
    response: Any, request_latency: float, kwargs: dict
) -> ChatCompletion:
    model_requested = kwargs["model"]
    if type(response) is LegacyAPIResponse:
        http_response = response.http_response.json()
        model_used = http_response.get("model")
        scope3_row = ImpactRow(
            model_id=model_requested,
            model_used_id=model_used,
            input_tokens=http_response.get("usage").get("prompt_tokens"),
            output_tokens=http_response.get("usage").get("completion_tokens"),
            request_duration_ms=request_latency * 1000,
            managed_service_id=PROVIDER,
        )
        messages = kwargs.get("messages", [])
        for message in messages:
            aggregate_multimodal(message, scope3_row, logger)
        Scope3AI.get_instance().submit_impact(scope3_row)
        return response
    else:
        model_used = response.model
        scope3_row = ImpactRow(
            model_id=model_requested,
            model_used_id=model_used,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            request_duration_ms=request_latency * 1000,
            managed_service_id=PROVIDER,
        )
        messages = kwargs.get("messages", [])
        for message in messages:
            aggregate_multimodal(message, scope3_row, logger)
        scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)

    # analyse multimodal part


def openai_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: Completions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    return _openai_chat_wrapper(response, request_latency, kwargs)


def openai_chat_wrapper_stream(
    wrapped: Callable,
    instance: Completions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> Stream[ChatCompletionChunk]:
    timer_start = time.perf_counter()
    if "stream_options" not in kwargs:
        kwargs["stream_options"] = {}
    if "include_usage" not in kwargs["stream_options"]:
        kwargs["stream_options"]["include_usage"] = True
    elif not kwargs["stream_options"]["include_usage"]:
        raise ValueError("stream_options include_usage must be True")

    stream = wrapped(*args, **kwargs)
    model_requested = kwargs["model"]

    for chunk in stream:
        request_latency = time.perf_counter() - timer_start

        if chunk.usage is not None:
            model_used = chunk.model

            scope3_row = ImpactRow(
                model_id=model_requested,
                model_used_id=model_used,
                input_tokens=chunk.usage.prompt_tokens,
                output_tokens=chunk.usage.completion_tokens,
                request_duration_ms=request_latency
                * 1000,  # TODO: can we get the header that has the processing time
                managed_service_id=PROVIDER,
            )

            scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
            yield ChatCompletionChunk(**chunk.model_dump(), scope3ai=scope3_ctx)
        else:
            yield chunk


async def openai_async_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: AsyncCompletions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
    timer_start = time.perf_counter()
    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    return _openai_chat_wrapper(response, request_latency, kwargs)


async def openai_async_chat_wrapper_stream(
    wrapped: Callable,
    instance: AsyncCompletions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> AsyncStream[ChatCompletionChunk]:
    timer_start = time.perf_counter()
    if "stream_options" not in kwargs:
        kwargs["stream_options"] = {}
    if "include_usage" not in kwargs["stream_options"]:
        kwargs["stream_options"]["include_usage"] = True
    elif not kwargs["stream_options"]["include_usage"]:
        raise ValueError("stream_options include_usage must be True")

    stream = await wrapped(*args, **kwargs)
    model_requested = kwargs["model"]

    async for chunk in stream:
        request_latency = time.perf_counter() - timer_start

        if chunk.usage is not None:
            model_used = chunk.model

            scope3_row = ImpactRow(
                model_id=model_requested,
                model_used_id=model_used,
                input_tokens=chunk.usage.prompt_tokens,
                output_tokens=chunk.usage.completion_tokens,
                request_duration_ms=request_latency
                * 1000,  # TODO: can we get the header that has the processing time
                managed_service_id=PROVIDER,
            )

            scope3_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
            yield ChatCompletionChunk(**chunk.model_dump(), scope3ai=scope3_ctx)
        else:
            yield chunk


async def openai_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncCompletions,
    args: Any,
    kwargs: Any,
) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
    # if litellm_response_enabled():
    #     return wrapped(*args, **kwargs)
    if kwargs.get("stream", False):
        return openai_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await openai_async_chat_wrapper_non_stream(
            wrapped, instance, args, kwargs
        )


def openai_chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
    # if litellm_response_enabled():
    #     return wrapped(*args, **kwargs)
    if kwargs.get("stream", False):
        return openai_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return openai_chat_wrapper_non_stream(wrapped, instance, args, kwargs)
