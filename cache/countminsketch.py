import numpy as np
import mmh3


class CountMinSketch:

    def __init__(self, width, depth=4):
        self.depth = depth
        self.width = width
        self.table = np.zeros((depth, width))
        self.keys = set()
        self.hash_functions = self.__hash

    def update(self, item, count=1):
        for table, i in zip(self.table, self.hash_functions(item, self.depth, self.width)):
            table[i] += count

    def estimate(self, item):
        return min(table[i] for table, i in zip(self.table, self.hash_functions(item, self.depth, self.width)))

    def reset(self):
        self.table = np.zeros((self.depth, self.width))

    def __hash(self, item, depth, width):
        for i in range(depth):
            index = mmh3.hash64(item, signed=False)[0] % width
            yield index
