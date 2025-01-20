import contextlib
import contextvars
from typing import Any, Callable

from aiohttp import ClientSession

AIOHTTP_RESPONSE_BASEKEY = "scope3ai__aiohttp_interceptor"
AIOHTTP_RESPONSE_ENABLED = contextvars.ContextVar(
    f"{AIOHTTP_RESPONSE_BASEKEY}__enabled", default=False
)
AIOHTTP_RESPONSE_VALUE = contextvars.ContextVar[Any](
    f"{AIOHTTP_RESPONSE_BASEKEY}__value", default=None
)


def aiohttp_response_enabled():
    return AIOHTTP_RESPONSE_ENABLED.get() is True


async def aiohttp_response_wrapper(
    wrapped: Callable, instance: ClientSession, args: Any, kwargs: Any
):
    response = await wrapped(*args, **kwargs)
    context_var_value = AIOHTTP_RESPONSE_VALUE.get()
    if context_var_value is None:
        context_var_value = []
    context_var_value.append(response)
    AIOHTTP_RESPONSE_VALUE.set(context_var_value)
    return response


@contextlib.contextmanager
def aiohttp_response_capture():
    try:
        AIOHTTP_RESPONSE_VALUE.set(None)
        AIOHTTP_RESPONSE_ENABLED.set(True)
        yield AIOHTTP_RESPONSE_VALUE
    finally:
        AIOHTTP_RESPONSE_ENABLED.set(False)
