import time
from typing import Any, Callable, Optional, Union

from wrapt import wrap_function_wrapper

from scope3ai.lib import Scope3AI
from scope3ai.api.types import Scope3AIContext, Model, ImpactRow

try:
    from openai import AsyncStream, Stream
    from openai.resources.chat import AsyncCompletions, Completions
    from openai.types.chat import ChatCompletion as _ChatCompletion
    from openai.types.chat import ChatCompletionChunk as _ChatCompletionChunk
except ImportError:
    AsyncStream = object()
    Stream = object()
    AsyncCompletions = object()
    Completions = object()
    _ChatCompletion = object()
    _ChatCompletionChunk = object()

PROVIDER = "huggingface"


class ChatCompletion(_ChatCompletion):
    scope3ai: Optional[Scope3AIContext] = None


class ChatCompletionChunk(_ChatCompletionChunk):
    scope3ai: Optional[Scope3AIContext] = None


def huggingface_chat_wrapper(
    wrapped: Callable, instance: Completions, args: Any, kwargs: Any
) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
    if kwargs.get("stream", False):
        return hugging_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return hugging_chat_wrapper_non_stream(wrapped, instance, args, kwargs)


def hugging_chat_wrapper_non_stream(
    wrapped: Callable,
    instance: Completions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
    timer_start = time.perf_counter()
    response = wrapped(*args, **kwargs)
    request_latency = time.perf_counter() - timer_start

    model_requested = kwargs["model"]
    model_used = response.model

    scope3_row = ImpactRow(
        model=Model(id=model_requested),
        model_used=Model(id=model_used),
        input_tokens=response.usage.prompt_tokens,
        output_tokens=response.usage.completion_tokens,
        request_duration_ms=request_latency * 1000,
        managed_service_id=PROVIDER,
    )

    scope3ai_ctx = Scope3AI.get_instance().submit_impact(scope3_row)
    return ChatCompletion(**response.model_dump(), scope3ai=scope3ai_ctx)


def hugging_chat_wrapper_stream(
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
    for i, chunk in enumerate(stream):
        request_latency = time.perf_counter() - timer_start
        if chunk.usage is not None:
            model_requested = kwargs["model"]
            model_used = chunk.model

            scope3_row = ImpactRow(
                model=Model(id=model_requested),
                model_used=Model(id=model_used),
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


async def hugging_async_chat_wrapper(
    wrapped: Callable,
    instance: AsyncCompletions,
    args: Any,
    kwargs: Any,
) -> Union[ChatCompletion, AsyncStream[ChatCompletionChunk]]:
    if kwargs.get("stream", False):
        return hugging_async_chat_wrapper_stream(wrapped, instance, args, kwargs)
    else:
        return await hugging_async_chat_wrapper_base(wrapped, instance, args, kwargs)


async def hugging_async_chat_wrapper_base(
    wrapped: Callable,
    instance: AsyncCompletions,  # noqa: ARG001
    args: Any,
    kwargs: Any,
) -> ChatCompletion:
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
    return ChatCompletion(**response.model_dump(), scope3ai=scope3_ctx)


async def hugging_async_chat_wrapper_stream(
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
    i = 0
    token_count = 0
    model_requested = kwargs["model"]
    async for chunk in stream:
        if i == 0 and chunk.model == "":
            continue
        if i > 0 and chunk.choices[0].finish_reason is None:
            token_count += 1
        request_latency = time.perf_counter() - timer_start
        model_used = chunk.model

        if chunk.usage is not None:
            scope3_row = ImpactRow(
                model=Model(id=model_requested),
                model_used=Model(id=model_used),
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
        i += 1


class HuggingFaceInstrumentor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "module": "huggingface_hub.inference._client.InferenceClient",
                "name": "Completions.create",
                "wrapper": huggingface_chat_wrapper,
            },
            {
                "module": "openai.resources.chat.completions",
                "name": "AsyncCompletions.create",
                "wrapper": hugging_async_chat_wrapper,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )
