import contextlib
import contextvars

HFRS_BASEKEY = "scope3ai__huggingface__hf_raise_for_status"
HFRS_ENABLED = contextvars.ContextVar(f"{HFRS_BASEKEY}__enabled", default=None)
HFRS_VALUE = contextvars.ContextVar(f"{HFRS_BASEKEY}__value", default=None)


def hf_raise_for_status_enabled():
    return HFRS_ENABLED.get() is True


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
