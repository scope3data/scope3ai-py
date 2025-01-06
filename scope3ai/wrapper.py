from wrapt import resolve_path
from wrapt import wrap_object as _wrap_object


def wrap_object(module, name, factory, args=(), kwargs={}):
    # prevent installing the wrapper twice
    parentr, attribute, original = resolve_path(module, name)
    wrapper = args[0]

    if isinstance(original, factory) and original._self_wrapper == wrapper:
        return

    return _wrap_object(module, name, factory, args, kwargs)
