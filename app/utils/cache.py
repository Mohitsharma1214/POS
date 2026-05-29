# app/utils/cache.py
"""Simple in-memory TTL cache for async functions.
Usage:
    @ttl_cache(ttl_seconds=300)
    async def fetch_something(...): ...
"""
import asyncio
import time
from functools import wraps
from typing import Callable, Any

def ttl_cache(ttl_seconds: int = 300):
    """Decorator that caches the result of an async function for ``ttl_seconds``.
    The cache key is based on the function name and its positional/keyword arguments.
    """
    _cache = {}
    _lock = asyncio.Lock()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = (func.__name__, args, frozenset(kwargs.items()))
            # --- Check cache (brief lock, never held across an await) ---
            async with _lock:
                entry = _cache.get(key)
                now = time.time()
                if entry and now - entry[0] < ttl_seconds:
                    return entry[1]
            # --- Call the function WITHOUT holding the lock ---
            # Multiple concurrent callers with the same uncached key may all
            # execute; the last writer wins, which is safe for idempotent calls.
            result = await func(*args, **kwargs)
            # --- Write result back (brief lock) ---
            async with _lock:
                _cache[key] = (time.time(), result)
            return result
        return wrapper
    return decorator
