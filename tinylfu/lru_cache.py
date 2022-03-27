from collections import OrderedDict
from typing import Optional, Tuple, Any


class LRUCache:

    def __init__(self, capacity=128):
        self.cache = OrderedDict()
        self.size = capacity

    def __contains__(self, item) -> bool:
        return item in self.cache

    def __len__(self) -> int:
        return len(self.cache)

    def is_full(self) -> bool:
        return len(self.cache) == self.size

    def get(self, key: str) -> Optional[Any]:
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(key)  # Gotta keep this pair fresh, move to end of OrderedDict
            return self.cache[key]

    def set(self, key: str, value: int) -> Optional[Tuple[Any, Any]]:

        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.size:
            return self.cache.popitem(last=False)

        return None, None

    def remove(self, key) -> Optional[Tuple[Any, Any]]:
        if key in self.cache:
            return self.cache.popitem(key)

        return None

    def get_victim(self) -> Optional[Tuple[Any, Any]]:
        if self.size == len(self.cache):
            oldest = next(iter(self.cache))
            return oldest

        return None
