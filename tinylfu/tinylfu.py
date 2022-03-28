import functools
import math
from collections import defaultdict

from countminsketch import CountMinSketch
from doorkeeper import Doorkeeper
from lru_cache import LRUCache
from slru import SLRUCache
from statistics import Statistics


def monitor_function(get_func):
    """
    Decorator function to monitor the statistics of the cache.
    """
    @functools.wraps(get_func)
    def _impl(self, key):
        if not self.statistics:
            return get_func(self, key)
        self.statistics.keys.add(key)
        self.statistics.total_access += 1
        self.keys_statistics[key]["accesses"] += 1
        result = get_func(self, key)
        if result:
            self.keys_statistics[key]["hits"] += 1
            self.statistics.total_hits += 1
        else:
            self.keys_statistics[key]["misses"] += 1
        return result

    return _impl


def tinylfu_cache(user_function, maxsize=1000000, sample=100000, false_positive=0.01):
    """
    Decorator function to cache the result of the given user function.
    :param user_function: function to cache.
    :param maxsize: size of the cache.
    :param sample: sample size.
    :param false_positive: false positive rate for the admission window.
    :return:
    """
    cache = TinyLFU(maxsize, sample, false_positive)

    @functools.wraps(user_function)
    def _tinylfu_cache_wrapper(*args, **kwargs):
        try:
            key = hash((args, kwargs))
        except TypeError:
            key = repr((args, kwargs))
        if key in cache:
            return cache[key]
        cache[key] = user_function(*args, **kwargs)
        return cache[key]

    return _tinylfu_cache_wrapper


class TinyLFU:

    def __init__(self, size=1000000, sample=100000, false_positive=0.01):
        self.size = size
        self.__sample = sample
        self.__age = 0
        self.doorkeeper = Doorkeeper(sample, false_positive)
        self.bouncer = CountMinSketch(size)

        self.lru_pct = 1
        self.lru_size = (self.lru_pct * size) / 100
        if self.lru_size < 1:
            self.lru_size = 1
        self.lru = LRUCache(self.lru_size)

        self.slru_size = math.ceil(size * ((100 - self.lru_pct) / 100))
        if self.slru_size < 1:
            self.slru_size = 1
        self.slru20 = math.ceil(0.2 * self.slru_size)
        if self.slru20 < 1:
            self.slru20 = 1
        self.slru = SLRUCache(self.slru20, self.slru_size - self.slru20)

        self.statistics = None
        self.keys_statistics = defaultdict(lambda: {"hits": 0, "misses": 0, "accesses": 0}, hits=0, misses=0,
                                           accesses=0)

    @monitor_function
    def __getitem__(self, key: str) -> object:
        """
        Get the key and update the frequencies following the tinyLFU scheme.
        """
        self.__age += 1
        if self.__age == self.__sample:
            self.bouncer.reset()
            self.doorkeeper.reset()
            self.__age = 0

        self.bouncer.update(key)

        value = self.lru.get(key)
        if value:
            return value

        value = self.slru.get(key)
        if value:
            return value

    def __setitem__(self, key: str, value: object) -> None:
        """
        Set the key, value pair in the cache and update it following the tinyLFU scheme.
        """
        if key in self.slru:
            self.slru.remove(key)

        old_key, old_value = self.lru.set(key, value)
        if not old_key:
            return
        victim_key = self.slru.get_victim()
        if not victim_key:
            self.slru.set(old_key, old_value)
            return

        if not self.doorkeeper.allow(old_key):
            return

        victim_count = self.bouncer.estimate(victim_key)
        item_count = self.bouncer.estimate(old_key)
        if victim_count < item_count:
            self.slru.set(old_key, old_value)
        else:
            return

    def remove(self, key: str) -> object:
        """
        Remove key from the cache and return the value. If the key is not in the cache, return None.
        """
        value = self.lru.remove(key)
        if value:
            return value

        value = self.slru.remove(key)
        if value:
            return value

    def monitor(self, *keys) -> Statistics:
        """
        Start monitoring statistics related to the given keys. If no key is no provided, monitor only general statistics.
        :param keys: list of keys to monitor
        :return: Statistics object related to this cache instance.
        """
        self.statistics = Statistics(self, keys)
        return self.statistics

    def hit_rate_key(self, key: str) -> float:
        """
        Return the hit rate related to the given key.
        """
        if not self.statistics:
            raise NotImplementedError
        if key in self.keys_statistics:
            return (self.keys_statistics[key]["hits"] / self.keys_statistics[key]["accesses"]) * 100
        return 0

    def miss_rate_key(self, key: str) -> float:
        """Return the miss rate related to the given key."""
        if not self.statistics:
            raise NotImplementedError

        return (1 - self.keys_statistics[key]["hits"] / self.keys_statistics[key]["accesses"]) * 100

    def __contains__(self, item: str) -> bool:
        return item in self.lru or item in self.slru

    def __len__(self) -> int:
        return len(self.lru) + len(self.slru)


def main():
    @tinylfu_cache
    def fib(n):
        if n in [1, 2]:
            return 1
        return fib(n - 1) + fib(n - 2)

    print('250th fibonacci number:', fib(250))
    return 0

