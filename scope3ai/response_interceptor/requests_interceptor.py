import contextlib
import contextvars
from typing import Any, Callable

from requests import Session

REQUESTS_RESPONSE_BASEKEY = "scope3ai__requests_interceptor"
REQUESTS_RESPONSE_ENABLED = contextvars.ContextVar(
    f"{REQUESTS_RESPONSE_BASEKEY}__enabled", default=None
)
REQUESTS_RESPONSE_VALUE = contextvars.ContextVar(
    f"{REQUESTS_RESPONSE_BASEKEY}__value", default=None
)


def requests_response_enabled():
    return REQUESTS_RESPONSE_ENABLED.get() is True


def requests_response_wrapper(
    wrapped: Callable, instance: Session, args: Any, kwargs: Any
):
    response = wrapped(*args, **kwargs)
    context_var_value = REQUESTS_RESPONSE_VALUE.get()
    if context_var_value is None:
        context_var_value = []
    context_var_value.append(response)
    REQUESTS_RESPONSE_VALUE.set(context_var_value)
    return response


@contextlib.contextmanager
def requests_response_capture():
    try:
        REQUESTS_RESPONSE_VALUE.set(None)
        REQUESTS_RESPONSE_ENABLED.set(True)
        yield REQUESTS_RESPONSE_VALUE
    finally:
        REQUESTS_RESPONSE_ENABLED.set(False)
