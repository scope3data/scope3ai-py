from wrapt import wrap_function_wrapper


class BaseTracer:
    wrapper_methods = []

    def instrument(self) -> None:
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"],
                wrapper["name"],
                wrapper["wrapper"],
            )
