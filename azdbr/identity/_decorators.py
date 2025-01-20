import functools


def func_decorator(func):
    """
    Function decorator - for now, it updates the function name into the kwargs and returns
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs["d_name"] = func.__qualname__
        return func(*args, **kwargs)

    return wrapper
