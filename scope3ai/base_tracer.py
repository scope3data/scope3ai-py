from wrapt import wrap_function_wrapper

from scope3ai.constants import CLIENTS


# TODO Tracer is not BaseTracer?
class BaseTracer:
    wrapper_methods = []
    client: CLIENTS

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"],
                wrapper["name"],
                wrapper["wrapper"],
            )
