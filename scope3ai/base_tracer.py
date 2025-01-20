from typing import Callable

from wrapt import wrap_function_wrapper

from scope3ai.tracers.utils.litellm_context import is_litellm_active


def is_using_lite_llm_decorator(func):
    def wrapper(wrapped: Callable, instance: any, args: any, kwargs: any):
        if is_litellm_active():
            return wrapped(*args, **kwargs)
        else:
            return func(wrapped, instance, *args, **kwargs)

    return wrapper


class BaseTracer:
    wrapper_methods = []

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"],
                wrapper["name"],
                is_using_lite_llm_decorator(wrapper["wrapper"]),
            )
