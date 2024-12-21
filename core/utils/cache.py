import hashlib

from config.env import env
from django.core.cache import cache


class Cache:
    def remember(self, func, key: str, timeout=None, *args, **kwargs):
        cache_enabled = env.bool("CACHE_ENABLED")
        key = hashlib.md5(key.encode("utf-8")).hexdigest()
        response = cache.get(key)

        if not cache_enabled:
            return func(*args, **kwargs)
        elif response is None:
            response = func(*args, **kwargs)
            cache.set(key, response, env.int("CACHE_TIME") if timeout is None else timeout)

        return response
