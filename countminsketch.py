import numpy as np
import mmh3


class CountMinSketch:

    def __init__(self, width, depth=4):
        self.depth = depth
        self.width = width
        self.table = np.zeros((depth, width))
        self.hash_functions = _hash

    def update(self, item, count=1):
        for table, i in zip(self.table, self.hash_functions(item, self.depth, self.width)):
            table[i] += count

    def estimate(self, item):
        return min(table[i] for table, i in zip(self.table, self.hash_functions(item, self.depth, self.width)))

    def reset(self):
        self.table = np.zeros((self.depth, self.width))


def _hash(item, depth, width):
    for i in range(depth):
        index = mmh3.hash64(item, signed=False)[0] % width
        yield index


if __name__ == "__main__":
    cm4 = CountMinSketch(16, 4)
    cm4.update("dog")
    print(cm4.estimate("dog"))
