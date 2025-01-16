import time
from collections.abc import AsyncIterable, Iterable
from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional, Union

import tiktoken
from huggingface_hub import (  # type: ignore[import-untyped]
    AsyncInferenceClient,
    InferenceClient,
)
from huggingface_hub import ChatCompletionOutput as _ChatCompletionOutput
from huggingface_hub import ChatCompletionStreamOutput as _ChatCompletionStreamOutput
from requests import Response

from scope3ai.api.types import ImpactRow, Scope3AIContext
from scope3ai.constants import PROVIDERS
from scope3ai.lib import Scope3AI
from scope3ai.response_interceptor.requests_interceptor import requests_response_capture

PROVIDER = PROVIDERS.HUGGINGFACE_HUB.value
HUGGING_FACE_CHAT_TASK = "chat"


@dataclass
class ChatCompletionOutput(_ChatCompletionOutput):
    scope3ai: Optional[Scope3AIContext] = None


@dataclass
class ChatCompletionStreamOutput(_ChatCompletionStreamOutput):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_chat_wrapper(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> Union[ChatCompletionOutput, Iterable[ChatCompletionStreamOutput]]:
    if kwargs.get("stream", False):
        return huggingface_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return huggingface_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def huggingface_chat_wrapper_non_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> ChatCompletionOutput:
    timer_start = time.perf_counter()
    http_response: Response | None = None
    with requests_response_capture() as responses:
        response = wrapped(*args, **kwargs)
        http_responses = responses.get()
        if http_responses:
            http_response = http_responses[0]
    model = (
        instance.model
        or kwargs.get("model")
        or instance.get_recommended_model(HUGGING_FACE_CHAT_TASK)
    )
    if http_response:
        compute_time = http_response.headers.get("x-compute-time")
    else:
        compute_time = time.perf_counter() - timer_start
    scope3_row = ImpactRow(
        model_id=model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    chat = ChatCompletionOutput(**asdict(response))
    chat.scope3ai = scope3ai_ctx
    return chat


def huggingface_chat_wrapper_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> Iterable[ChatCompletionStreamOutput]:
    timer_start = time.perf_counter()
    stream = wrapped(*args, **kwargs)
    token_count = 0
    model = (
        instance.model
        or kwargs.get("model")
        or instance.get_recommended_model(HUGGING_FACE_CHAT_TASK)
    )
    for chunk in stream:
        token_count += 1
        request_latency = time.perf_counter() - timer_start
        scope3_row = ImpactRow(
            model_id=model,
            output_tokens=token_count,
            request_duration_ms=request_latency * 1000,
            managed_service_id=PROVIDER,
        )
        chunk_data = ChatCompletionStreamOutput(**asdict(chunk))
        scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        if scope3_ctx is not None:
            chunk_data.scope3ai = scope3_ctx
        yield chunk_data


async def huggingface_async_chat_wrapper(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> Union[ChatCompletionOutput, AsyncIterable[ChatCompletionStreamOutput]]:
    if kwargs.get("stream", False):
        return huggingface_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await huggingface_async_chat_wrapper_non_stream(
            wrapped, instance, args, kwargs
        )


async def huggingface_async_chat_wrapper_non_stream(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> ChatCompletionOutput:
    timer_start = time.perf_counter()

    response = await wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start
    model = (
        instance.model or kwargs.get("model") or instance.get_recommended_model("chat")
    )
    encoder = tiktoken.get_encoding("cl100k_base")
    output_tokens = len(encoder.encode(response.choices[0].message.content))
    scope3_row = ImpactRow(
        model_id=model,
        input_tokens=response.usage.prompt_tokens,
        output_tokens=output_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )

    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    chat = ChatCompletionOutput(**asdict(response))
    chat.scope3ai = scope3ai_ctx
    return chat


# Todo: How headers works for stream
async def huggingface_async_chat_wrapper_stream(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> AsyncIterable[ChatCompletionStreamOutput]:
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    token_count = 0
    model = instance.model or kwargs["model"]
    async for chunk in stream:
        token_count += 1
        request_latency = time.perf_counter() - timer_start
        scope3_row = ImpactRow(
            model_id=model,
            output_tokens=token_count,
            request_duration_ms=request_latency
            * 1000,  # TODO: can we get the header that has the processing time
            managed_service_id=PROVIDER,
        )
        scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        chunk_data = ChatCompletionStreamOutput(**asdict(chunk))
        if scope3_ctx is not None:
            chunk_data.scope3ai = scope3_ctx
        yield chunk_data
