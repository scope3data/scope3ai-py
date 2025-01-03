import contextlib
import contextvars

HFRS_BASEKEY = "scope3ai__huggingface__hf_raise_for_status"
HFRS_ENABLED = contextvars.ContextVar(f"{HFRS_BASEKEY}__enabled", default=None)
HFRS_VALUE = contextvars.ContextVar(f"{HFRS_BASEKEY}__value", default=None)


HFRS_ASYNC_BASEKEY = "scope3ai__huggingface__hf_async_raise_for_status"
HFRS_ASYNC_ENABLED = contextvars.ContextVar(
    f"{HFRS_ASYNC_BASEKEY}__enabled", default=None
)
HFRS_ASYNC_VALUE = contextvars.ContextVar(f"{HFRS_ASYNC_BASEKEY}__value", default=None)


def hf_raise_for_status_enabled():
    return HFRS_ENABLED.get() is True


def hf_async_raise_for_status_enabled():
    return HFRS_ASYNC_ENABLED.get() is True


def hf_raise_for_status_wrapper(wrapped, instance, args, kwargs):
    try:
        result = wrapped(*args, **kwargs)
        response = args[0]
        HFRS_VALUE.set(response)
        return result
    except Exception as e:
        raise e


@contextlib.contextmanager
def hf_raise_for_status_capture():
    try:
        HFRS_VALUE.set(None)
        HFRS_ENABLED.set(True)
        yield HFRS_VALUE
    finally:
        HFRS_ENABLED.set(False)


@contextlib.contextmanager
def hf_async_raise_for_status_capture():
    try:
        HFRS_ASYNC_VALUE.set(None)
        HFRS_ASYNC_ENABLED.set(True)
        yield HFRS_ASYNC_VALUE
    finally:
        HFRS_ASYNC_ENABLED.set(False)


def async_post_wrapper(session_post):
    async def wrapped_post(*args, **kwargs):
        result = await session_post(*args, **kwargs)
        HFRS_ASYNC_VALUE.set(result)
        return result

    return wrapped_post


def get_client_session_async_wrapper(wrapped, instance, args, kwargs):
    try:
        result = wrapped(*args, **kwargs)
        result.post = async_post_wrapper(result.post)
        return result
    except Exception as e:
        raise e
