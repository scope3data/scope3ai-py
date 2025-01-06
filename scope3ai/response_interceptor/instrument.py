import importlib.metadata
import importlib.util

from scope3ai.wrapper import wrap_object  # type: ignore[import-untyped]
from wrapt import FunctionWrapper

from scope3ai.response_interceptor.aiohttp_interceptor import (
    aiohttp_response_wrapper,
    aiohttp_response_enabled,
)
from scope3ai.response_interceptor.requests_interceptor import (
    requests_response_wrapper,
    requests_response_enabled,
)


class ResponseInterceptor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "library": "aiohttp",
                "module": "client",
                "name": "ClientSession._request",
                "wrapper": aiohttp_response_wrapper,
                "enabled": aiohttp_response_enabled,
            },
            {
                "library": "requests",
                "module": "sessions",
                "name": "Session.send",
                "wrapper": requests_response_wrapper,
                "enabled": requests_response_enabled,
            },
        ]

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            if importlib.util.find_spec(wrapper["library"]) is not None:
                wrap_object(
                    "{}.{}".format(wrapper["library"], wrapper["module"]),
                    wrapper["name"],
                    FunctionWrapper,
                    (wrapper["wrapper"], wrapper["enabled"]),
                )
