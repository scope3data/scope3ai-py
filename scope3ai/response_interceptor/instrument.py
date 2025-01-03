import importlib.metadata
import importlib.util

from wrapt import wrap_object, FunctionWrapper  # type: ignore[import-untyped]

from scope3ai.response_interceptor.aiohttp_interceptor import aiohttp_request_wrapper


class ResponseInterceptor:
    def __init__(self) -> None:
        self.wrapped_methods = [
            {
                "library": "aiohttp",
                "module": "client",
                "name": "ClientSession._request",
                "wrapper": aiohttp_request_wrapper,
                "enabled": True,
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
