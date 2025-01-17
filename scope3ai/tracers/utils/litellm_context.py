import contextvars

LITELLM_RESPONSE_BASEKEY = "scope3ai__litellm_interceptor"
LITELLM_ENABLED = contextvars.ContextVar(
    f"{LITELLM_RESPONSE_BASEKEY}__enabled", default=None
)


def litellm_response_enabled() -> bool:
    return LITELLM_ENABLED.get() is True


def litellm_switch():
    LITELLM_ENABLED.set(not litellm_response_enabled())
