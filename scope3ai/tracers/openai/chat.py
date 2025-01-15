import base64
import logging
import time
from io import BytesIO
from typing import Any, Callable, Optional, Union

from openai import AsyncStream, Stream
from openai.resources.chat import AsyncCompletions, Completions
from openai.types.chat import ChatCompletion as _ChatCompletion
from openai.types.chat import ChatCompletionChunk as _ChatCompletionChunk

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI

from .utils import MUTAGEN_MAPPING, _get_audio_duration

PROVIDER = PROVIDERS.OPENAI.value
logger = logging.getLogger("scope3ai.tracers.openai.chat")


class ChatCompletion(_ChatCompletion):
    scope3ai: Optional[Scope3AIContext] = None


class ChatCompletionChunk(_ChatCompletionChunk):
    scope3ai: Optional[Scope3AIContext] = None


def _openai_aggregate_multimodal_image(content: dict, row: ImpactRow) -> None:
    from PIL import Image

    url = content["image_url"]["url"]
    if url.startswith("data:"):
        # extract content type, and data part
        # example: data:image/jpeg;base64,....
        content_type, data = url.split(",", 1)
        image_data = BytesIO(base64.b64decode(data))
        image = Image.open(image_data)
        width, height = image.size
        size = f"{width}x{height}"

        if row.input_images is None:
            row.input_images = size
        else:
            row.input_images += f",{size}"

    else:
        # TODO: not supported yet.
        # Should we actually download the file here just to have the size ??
        pass


def _openai_aggregate_multimodal_audio(content: dict, row: ImpactRow) -> None:
    input_audio = content["input_audio"]
    format = input_audio["format"]
    b64data = input_audio["data"]
    assert format in MUTAGEN_MAPPING

    # decode the base64 data
    audio_data = base64.b64decode(b64data)
    duration = _get_audio_duration(format, audio_data)

    if row.input_audio_seconds is None:
        row.input_audio_seconds = duration
    else:
        row.input_audio_seconds += duration


def _openai_aggregate_multimodal_content(content: dict, row: ImpactRow) -> None:
    try:
        content_type = content.get("type")
        if content_type == "image_url":
            _openai_aggregate_multimodal_image(content, row)
        elif content_type == "input_audio":
            _openai_aggregate_multimodal_audio(content, row)
    except Exception as e:
        logger.error(f"Error processing multimodal content: {e}")


def _openai_aggregate_multimodal(message: dict, row: ImpactRow) -> None:
    # if the message content is not a tuple/list, it's just text.
    # so there is nothing multimodal in it, we can just forget about it.
    content = message.get("content", [])
    if isinstance(content, (tuple, list)):
        for item in content:
            _openai_aggregate_multimodal_content(item, row)


def _openai_chat_wrapper(
    response: Any, request_latency: float, kwargs: dict
) -> ChatCompletion:
    model_requested = kwargs["model"]
    model_used = response.model

    scope3_row = ImpactRow(
        model=model_requested,
        model_used=model_used,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )

    # analyse multimodal part
    messages = kwargs.get("messages", [])
    for message in messages:
        _openai_aggregate_multimodal(message, scope3_row)

    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)


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
                model=model_requested,
                model_used=model_used,
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
                model=model_requested,
                model_used=model_used,
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
