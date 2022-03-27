import functools
import math
from collections import defaultdict

from countminsketch import CountMinSketch
from doorkeeper import Doorkeeper
from lru_cache import LRUCache
from slru import SLRUCache
from statistics import Statistics

def wrapper(get_func):
    @functools.wraps(get_func)
    def _impl(self, key):
        if not self.statistics:
            return get_func
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

    @wrapper
    def get(self, key: str):
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

    def set(self, key: str, value):
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
        value = self.lru.remove(key)
        if value:
            return value

        value = self.slru.remove(key)
        if value:
            return value

    def monitor(self, keys=[]):
        self.statistics = Statistics(self, keys)
        return self.statistics

    def hit_rate_key(self, key):
        if not self.statistics:
            raise NotImplementedError
        if key in self.keys_statistics:
            return (self.keys_statistics[key]["hits"] / self.keys_statistics[key]["accesses"]) * 100
        return 0

    def miss_rate_key(self, key):
        if not self.statistics:
            raise NotImplementedError

        return (1 - self.keys_statistics[key]["hits"] / self.keys_statistics[key]["accesses"]) * 100
