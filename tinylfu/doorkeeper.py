import mmh3
from math import log2, ceil

from bitarray import bitarray


def hash_mm3_hash64(item, optimal_k, optimal_m):
    """Simple mmh3 hashing function that map the result to the given depth and width."""
    for i in range(optimal_k):
        bit_index = mmh3.hash64(item, signed=False)[0] % optimal_m
        yield bit_index


class BloomFilter:
    """Simple Bloom filter implementation for use in python,

       Args:
           num_elem (int): max number of elements in the bloom filter.
           false_positive_rate (float): false positive rate of the filter.
           hash_function (function): Hashing strategy function to use `hf(key, number)`
       Returns:
           BloomFilter: A BloomFilter object
    """

    def __init__(self, num_elem: int, false_positive_rate: float, hash_function=None):
        self.optimal_m = ceil((num_elem * abs(log2(false_positive_rate))) / log2(2) ** 2)
        self.optimal_k = ceil((self.optimal_m / num_elem) * log2(2))
        self.bits = bitarray(self.optimal_m)
        self.bits.setall(False)
        self.probe_function = hash_mm3_hash64 if not hash_function else hash_function

    def __contains__(self, item: object):
        return all(self.bits[i] for i in self.probe_function(item, self.optimal_k, self.optimal_m))

    def insert(self, other: object):
        """Insert object in the filter """
        for i in self.probe_function(other):
            self.bits[i] = True

    def clear(self):
        """Reset the filter to the starting state."""
        self.bits = bitarray(self.optimal_m)


class Doorkeeper:

    """Wrapper around the bloom filter"""

    def __init__(self, cap=100000, false_positive=0.01):
        self.filter = BloomFilter(cap, false_positive)

    def allow(self, key: str) -> bool:
        """Add the key and return True if the key was already present."""
        return self.__insert(key)

    def reset(self):
        """Reset the filter to the starting state."""
        self.filter.clear()

    def __insert(self, key: str) -> bool:
        """Add the key and return True if the key was already present."""
        already_present = key in self.filter
        self.filter.insert(key)
        return already_present

