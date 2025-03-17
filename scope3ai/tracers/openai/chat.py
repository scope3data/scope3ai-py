import logging
import time
from typing import Any, Callable, Optional, Union

from openai import AsyncStream, Stream
from openai._legacy_response import LegacyAPIResponse as _LegacyAPIResponse
from openai.resources.chat import AsyncCompletions, Completions
from openai.types.chat import ChatCompletion as _ChatCompletion
from openai.types.chat import ChatCompletionChunk as _ChatCompletionChunk

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.lib import Scope3AI
from scope3ai.constants import CLIENTS, try_provider_for_client
from scope3ai.tracers.utils.multimodal import (
    aggregate_multimodal,
    aggregate_multimodal_audio_content_output,
)


logger = logging.getLogger("scope3ai.tracers.openai.chat")


class LegacyApiResponse(_LegacyAPIResponse):
    scope3ai: Optional[Scope3AIContext] = None


class ChatCompletion(_ChatCompletion):
    scope3ai: Optional[Scope3AIContext] = None


class ChatCompletionChunk(_ChatCompletionChunk):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_chat_wrapper(
    response: Any, request_latency: float, kwargs: dict
) -> Union[_LegacyAPIResponse, ChatCompletion, ImpactRow]:
    model_requested = kwargs.get("model")
    modalities = kwargs.get("modalities", [])
    if type(response) is _LegacyAPIResponse:
        http_response = response.http_response.json()
        model_used = http_response.get("model")
        scope3_row = ImpactRow(
            managed_service_id=try_provider_for_client(CLIENTS.OPENAI),
            model_id=model_requested,
            model_used_id=model_used,
            input_tokens=http_response.get("usage", {}).get("prompt_tokens"),
            output_tokens=http_response.get("usage", {}).get("completion_tokens"),
            request_duration_ms=request_latency * 1000,
        )
        if "audio" in modalities:
            audio_format = kwargs.get("audio", {}).get("format", "mp3")
            for choice in http_response.get("choices", []):
                audio_data = choice.get("message", {}).get("audio", {})
                if audio_data:
                    audio_content = audio_data.get("data")
                    aggregate_multimodal_audio_content_output(
                        audio_content, audio_format, scope3_row
                    )

        messages = kwargs.get("messages", [])
        for message in messages:
            aggregate_multimodal(message, scope3_row, logger)
        return response, scope3_row
    else:
        scope3_row = ImpactRow(
            managed_service_id=try_provider_for_client(CLIENTS.OPENAI),
            model_id=model_requested,
            model_used_id=response.model,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            request_duration_ms=request_latency * 1000,
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

        messages = kwargs.get("messages", [])
        for message in messages:
            aggregate_multimodal(message, scope3_row, logger)
        return response, scope3_row

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
    response, scope3_row = _openai_chat_wrapper(response, request_latency, kwargs)
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    if isinstance(response, _LegacyAPIResponse):
        setattr(response, "scope3ai", scope3ai_ctx)
        return response
    else:
        return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)


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
                managed_service_id=try_provider_for_client(CLIENTS.OPENAI),
                model_id=model_requested,
                model_used_id=model_used,
                input_tokens=chunk.usage.prompt_tokens,
                output_tokens=chunk.usage.completion_tokens,
                request_duration_ms=request_latency
                * 1000,  # TODO: can we get the header that has the processing time
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
    response, scope3_row = _openai_chat_wrapper(response, request_latency, kwargs)
    scope3ai_ctx = await Scope3AI.get_instance().asubmit_impact(scope3_row)
    if isinstance(response, _LegacyAPIResponse):
        setattr(response, "scope3ai", scope3ai_ctx)
        return response
    else:
        return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)


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
                managed_service_id=try_provider_for_client(CLIENTS.OPENAI),
                model_id=model_requested,
                model_used_id=model_used,
                input_tokens=chunk.usage.prompt_tokens,
                output_tokens=chunk.usage.completion_tokens,
                request_duration_ms=request_latency
                * 1000,  # TODO: can we get the header that has the processing time
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
    if kwargs.get("stream", False):
        return openai_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await openai_async_chat_wrapper_non_stream(
            wrapped, instance, args, kwargs
        )


def openai_chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
    if kwargs.get("stream", False):
        return openai_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return openai_chat_wrapper_non_stream(wrapped, instance, args, kwargs)
