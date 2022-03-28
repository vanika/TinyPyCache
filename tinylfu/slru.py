from typing import Optional, Tuple, Any

from lru_cache import LRUCache


class SLRUCache:
    """
    An SLRU tinylfu item has the following lifecycle:

    New item is inserted to probational segment. This item becomes the most recently used item in the probational segment.

    If the probational segment is full, the least recently used item is evicted from tinylfu.
    If an item in the probational segment is accessed (with get or set), the item is migrate to the protected segment. This item becomes the most recently used item of the protected segment.

    If the protected segment is full, the least recently used item from the segment is moved to probational segment. This item becomes the most recently used item in the probational segment.
    If an item in the protected segment is accessed, it becomes the most recently used item of the protected segment.
    """

    def __init__(self, probation_cap=128, protected_cap=128):
        self.probation_cap = probation_cap
        self.protected_cap = protected_cap
        self.probational_cache = LRUCache(probation_cap)
        self.protected_cache = LRUCache(protected_cap)

    def __contains__(self, item) -> bool:
        return item in self.probational_cache or item in self.protected_cache

    def __len__(self) -> int:
        return len(self.probational_cache) + len(self.protected_cache)

    def is_full(self) -> bool:
        """Check if the cache is full."""
        return self.protected_cache.is_full() and self.probational_cache.is_full()

    def set(self, key, value):
        """Store a new views, potentially discarding an old value."""
        if key in self.protected_cache:
            self.protected_cache.set(key, value)

        elif key in self.probational_cache:
            self.probational_cache.remove(key)
            self.protected_cache.set(key, value)
        else:
            self.probational_cache.set(key, value)

    def get(self, key):
        """Store a new views, potentially discarding an old value."""
        if key in self.protected_cache:
            return self.protected_cache.get(key)

        if key in self.probational_cache:
            item_value = self.probational_cache.get(key)
            self.protected_cache.set(key, item_value)
            return item_value

        return None

    def remove(self, key: str):
        """Remove key from the cache. Return None if key is not present."""
        if key in self.protected_cache:
            return self.protected_cache.remove(key)
        if key in self.probational_cache:
            return self.probational_cache.remove(key)

        return None

    def get_victim(self) -> Optional[Tuple[Any, Any]]:
        """Get the last key:value pair in the cache. Cache is ordered following the SLRU scheme."""
        if len(self) >= (self.protected_cap + self.probation_cap):
            return self.probational_cache.get_victim()

        return None
