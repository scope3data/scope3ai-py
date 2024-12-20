import time
from collections.abc import AsyncIterable, Iterable
from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional, Union

from huggingface_hub import AsyncInferenceClient, InferenceClient  # type: ignore[import-untyped]
from huggingface_hub import ChatCompletionOutput as _ChatCompletionOutput
from huggingface_hub import ChatCompletionStreamOutput as _ChatCompletionStreamOutput

from scope3ai.api.types import Scope3AIContext, Model, ImpactRow
from scope3ai.lib import Scope3AI
from scope3ai.tracers.huggingface.utils import hf_raise_for_status_capture

PROVIDER = "huggingface_hub"


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
    with hf_raise_for_status_capture() as capture_response:
        response = wrapped(*args, **kwargs)
        http_response = capture_response.get()
    model_requested = instance.model
    model_used = response.model
    compute_time = http_response.headers.get("x-compute-time")
    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        model_used=Model(id=model_used),
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=float(compute_time) * 1000,
        managed_service_id=PROVIDER,
    )
    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return ChatCompletionOutput(**asdict(response), scope3ai=scope3ai_ctx)


def huggingface_chat_wrapper_stream(
    wrapped: Callable, instance: InferenceClient, args: Any, kwargs: Any
) -> Iterable[ChatCompletionStreamOutput]:
    timer_start = time.perf_counter()
    if "stream_options" not in kwargs:
        kwargs["stream_options"] = {}
    if "include_usage" not in kwargs["stream_options"]:
        kwargs["stream_options"]["include_usage"] = True
    elif not kwargs["stream_options"]["include_usage"]:
        raise ValueError("stream_options include_usage must be True")
    stream = wrapped(*args, **kwargs)
    token_count = 0
    model_request = instance.model
    model_used = instance.model
    for chunk in stream:
        token_count += 1
        request_latency = time.perf_counter() - timer_start
        scope3_row = ImpactRow(
            model=Model(id=model_request),
            model_used=Model(id=model_used),
            input_tokens=chunk.usage.prompt_tokens,
            output_tokens=chunk.usage.completion_tokens,
            request_duration_ms=request_latency,
            managed_service_id=PROVIDER,
        )
        scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        yield ChatCompletionStreamOutput(**asdict(chunk), scope3ai=scope3_ctx)


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
    model_requested = kwargs["model"]
    model_used = response.model

    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        model_used=Model(id=model_used),
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency
        * 1000,  # TODO: can we get the header that has the processing time
        managed_service_id=PROVIDER,
    )

    scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return ChatCompletionOutput(**asdict(response), scope3ai=scope3_ctx)


async def huggingface_async_chat_wrapper_stream(
    wrapped: Callable, instance: AsyncInferenceClient, args: Any, kwargs: Any
) -> AsyncIterable[ChatCompletionStreamOutput]:
    timer_start = time.perf_counter()
    stream = await wrapped(*args, **kwargs)
    token_count = 0
    model_request = kwargs["model"]
    model_used = instance.model
    async for chunk in stream:
        token_count += 1
        request_latency = time.perf_counter() - timer_start
        scope3_row = ImpactRow(
            model=Model(id=model_request),
            model_used=Model(id=model_used),
            input_tokens=chunk.usage.prompt_tokens,
            output_tokens=chunk.usage.completion_tokens,
            request_duration_ms=request_latency
            * 1000,  # TODO: can we get the header that has the processing time
            managed_service_id=PROVIDER,
        )
        scope3_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
        yield ChatCompletionStreamOutput(**asdict(chunk), scope3ai=scope3_ctx)
