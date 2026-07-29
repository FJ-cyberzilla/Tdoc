"""
Robustness Utilities.

Provides decorators and tools for error recovery and transient failure management.
"""

import functools
import time
from collections.abc import Callable


def retry(retries: int = 3, delay: int = 1, exceptions: tuple = (Exception,)):
    """
    Decorator to retry a function call on specific exceptions.
    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    time.sleep(delay)
            raise last_exception

        return wrapper

    return decorator
