"""
Robustness Utilities.

Provides decorators and tools for error recovery and transient failure management.
"""

import asyncio
import functools
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

# Type alias for clarity
FuncT = TypeVar("FuncT", bound=Callable[..., Coroutine[Any, Any, Any]])


def retry(
    retries: int = 3, delay: float = 1.0, exceptions: tuple[type[Exception], ...] = (Exception,)
):
    """
    Decorator to retry an async function call on specific exceptions.
    """

    def decorator(func: FuncT) -> FuncT:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for _attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    await asyncio.sleep(delay)
            if last_exception:
                raise last_exception
            raise RuntimeError("Retry failed")

        return wrapper  # type: ignore

    return decorator
