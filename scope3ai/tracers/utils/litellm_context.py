import contextlib
import contextvars

LITELLM_RESPONSE_BASEKEY = "scope3ai__litellm_interceptor"
LITELLM_ENABLED = contextvars.ContextVar(
    f"{LITELLM_RESPONSE_BASEKEY}__enabled", default=None
)


def litellm_response_enabled() -> bool:
    return LITELLM_ENABLED.get() is True


@contextlib.contextmanager
def litellm_active():
    try:
        LITELLM_ENABLED.set(True)
        yield LITELLM_ENABLED
    finally:
        LITELLM_ENABLED.set(False)
