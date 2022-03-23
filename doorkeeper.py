""" This is a bloom filter"""
from typing import Any
import mmh3
from math import log2, ceil

from bitarray import bitarray


class BloomFilter:

    def __init__(self, num_elem: int, false_positive_rate: float):
        self.optimal_m = ceil((num_elem * abs(log2(false_positive_rate))) / log2(2) ** 2)
        self.optimal_k = ceil((self.optimal_m / num_elem) * log2(2))
        self.bits = bitarray(self.optimal_m)
        self.bits.setall(False)
        self.probe_function = get_probes

    def insert(self, other):
        for i in self.probe_function(self, other):
            self.bits[i] = True

    def __contains__(self, item):
        return all(self.bits[i] for i in self.probe_function(self, item))

    def clear(self):
        self.bits = bitarray(self.optimal_m)


def get_probes(filter, item):
    for i in range(filter.optimal_k):
        bit_index = mmh3.hash64(item, signed=False)[0] % filter.optimal_m
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


if __name__ == '__main__':

    from random import sample
    from string import ascii_letters

    states = '''Alabama Alaska Arizona Arkansas California Colorado Connecticut
        Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas
        Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota
        Mississippi Missouri Montana Nebraska Nevada NewHampshire NewJersey
        NewMexico NewYork NorthCarolina NorthDakota Ohio Oklahoma Oregon
        Pennsylvania RhodeIsland SouthCarolina SouthDakota Tennessee Texas Utah
        Vermont Virginia Washington WestVirginia Wisconsin Wyoming'''.split()

    bf = BloomFilter(num_elem=300000, false_positive_rate=0.01, probe_function=get_probes)
    for state in states:
        bf.insert(state)

    m = sum(state in bf for state in states)
    print('%d true positives out of %d trials' % (m, len(states)))

    trials = 100000
    m = sum(''.join(sample(ascii_letters, 5)) in bf for i in range(trials))
    print('%d true negatives and %d false negatives out of %d trials'
          % (trials - m, m, trials))

    bf.clear()

    m = sum(state in bf for state in states)
    print('%d true positives out of %d trials' % (m, len(states)))
