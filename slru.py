"""
An SLRU cache item has the following lifecycle:

New item is inserted to probational segment. This item becomes the most recently used item in the probational segment.

If the probational segment is full, the least recently used item is evicted from cache.
If an item in the probational segment is accessed (with get or set), the item is migrate to the protected segment. This item becomes the most recently used item of the protected segment.

If the protected segment is full, the least recently used item from the segment is moved to probational segment. This item becomes the most recently used item in the probational segment.
If an item in the protected segment is accessed, it becomes the most recently used item of the protected segment.


"""
from lru_cache import LRUCache


class SLRUCache():

    def __init__(self, size=128):
        super().__init__(size)
        self.size = size
        self.probational_cache = LRUCache(size)
        self.protected_cache = LRUCache(size)

    def get(self, key: int) -> int:

        if key in self.probational_cache:
            item = self.probational_cache.get(key)
            evicted_key, evicted_value = self.protected_cache.put(key, item)
            if evicted_key and evicted_value:
                self.probational_cache.put(evicted_key, evicted_value)

            return item

        if key in self.protected_cache:
            return self.protected_cache.get(key)

    def put(self, key: int, value: int) -> None:

        self.probational_cache.put(key, value)

    def set(self, key: int, value: int) -> None:

        if key in self.protected_cache:
            self.protected_cache.set(key, value)
            return

        if key in self.probational_cache:
            self.probational_cache.pop(key)
            self.probational_cache.put(key, value)
            return


    def __contains__(self, item) -> bool:
        return item in self.probational_cache or item in self.protected_cache

    def __len__(self) -> int:
        return len(self.probational_cache) + len(self.protected_cache)

    def is_full(self) -> bool:
        return len(self.probational_cache) == self.size and len(self.protected_cache) == self.size
