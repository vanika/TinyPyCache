from collections import OrderedDict
from typing import Optional, Tuple, Any

from Cache import Cache


class LRUCache(Cache):

    def __init__(self, capacity=128):
        super().__init__(capacity)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)  # Gotta keep this pair fresh, move to end of OrderedDict
            return self.cache[key]

    def put(self, key: int, value: int) -> Optional[Tuple[Any, Any]]:

        evicted_key = evicted_value = None
        if key not in self.cache:
            if len(self.cache) >= self.size:
                evicted_key, evicted_value = self.cache.popitem(last=False)
        else:
            self.cache.move_to_end(key)  # Gotta keep this pair fresh, move to end of OrderedDict
            self.cache[key] = value

        return evicted_key, evicted_value

    def set(self, key, value) -> None:
        if key in self.cache:
            self.cache[key] = value

    def pop(self, key) -> Optional[Tuple[Any, Any]]:
        if key in self.cache:
            return self.cache.popitem(key)

        return None



