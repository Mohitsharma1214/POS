import asyncio

_cache = {}

async def cache_get(key):
    return _cache.get(key)

async def cache_set(key, value):
    _cache[key] = value
