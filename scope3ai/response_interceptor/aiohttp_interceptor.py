import contextlib
import contextvars
from typing import Any, Callable

from aiohttp import ClientSession

AIOHTTP_REQUEST_BASEKEY = "scope3ai__huggingface__hf_raise_for_status"
AIOHTTP_REQUESTS_ENABLED = contextvars.ContextVar(
    f"{AIOHTTP_REQUEST_BASEKEY}__enabled", default=None
)
AIOHTTP_REQUESTS_VALUE = contextvars.ContextVar(
    f"{AIOHTTP_REQUEST_BASEKEY}__value", default=None
)


def aiohttp_request_enabled():
    return AIOHTTP_REQUESTS_ENABLED.get() is True


async def aiohttp_request_wrapper(
    wrapped: Callable, instance: ClientSession, args: Any, kwargs: Any
):
    response = await wrapped(*args, **kwargs)
    context_var_value = AIOHTTP_REQUESTS_VALUE.get()
    if context_var_value is None:
        context_var_value = []
    context_var_value.append(response)
    AIOHTTP_REQUESTS_VALUE.set(context_var_value)
    return response


@contextlib.contextmanager
def aiohttp_requests_capture():
    try:
        AIOHTTP_REQUESTS_VALUE.set(None)
        AIOHTTP_REQUESTS_ENABLED.set(True)
        yield AIOHTTP_REQUESTS_VALUE
    finally:
        AIOHTTP_REQUESTS_ENABLED.set(False)
