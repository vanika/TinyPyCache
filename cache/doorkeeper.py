import mmh3
from math import log2, ceil

from bitarray import bitarray


class BloomFilter:

    def __init__(self, num_elem: int, false_positive_rate: float):
        self.optimal_m = ceil((num_elem * abs(log2(false_positive_rate))) / log2(2) ** 2)
        self.optimal_k = ceil((self.optimal_m / num_elem) * log2(2))
        self.bits = bitarray(self.optimal_m)
        self.bits.setall(False)
        self.probe_function = self.__get_probes

    def insert(self, other):
        for i in self.probe_function(other):
            self.bits[i] = True

    def __contains__(self, item):
        return all(self.bits[i] for i in self.probe_function(item))

    def clear(self):
        self.bits = bitarray(self.optimal_m)

    def __get_probes(self, item):
        for i in range(self.optimal_k):
            bit_index = mmh3.hash64(item, signed=False)[0] % self.optimal_m
            yield bit_index


class Doorkeeper:

    def __init__(self, cap=100000, false_positive=0.01):
        self.filter = BloomFilter(cap, false_positive)

    def __insert(self, key: str):
        already_present = key in self.filter
        self.filter.insert(key)
        return already_present

    def allow(self, key: str):
        return self.__insert(key)

    def reset(self):
        self.filter.clear()
