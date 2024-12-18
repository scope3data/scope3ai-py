from typing import Callable


async def hf_raise_for_status_wrapper(wrapped: Callable, *args, **kwargs) -> None:
    print("llega aca")
    print(args[0])
    wrapped(*args, **kwargs)
