import numpy as np
import mmh3


def hash_mmh3(item, depth, width):
    """Simple mmh3 hashing function" that map the result to the given depth and width."""
    for i in range(depth):
        index = mmh3.hash64(item, signed=False)[0] % width
        yield index


class CountMinSketch:
    """Simple Count-Min Sketch implementation for use in python,

       Args:
           width (int): The width of the count-min sketch
           depth (int): The depth of the count-min sketch (default is 4)
           hash_function (function): Hashing strategy function to use `hf(key, number)`
       Returns:
           CountMinSketch: A Count-Min Sketch object
    """

    def __init__(self, width, depth=4, hash_function=None):
        self.depth = depth
        self.width = width
        self.table = np.zeros((depth, width))
        self.keys = set()
        self.hash_functions = hash_mmh3 if not hash_function else hash_function

    def update(self, item, count=1):
        """Update the frequency of the item based on the given count."""
        for table, i in zip(self.table, self.hash_functions(item, self.depth, self.width)):
            table[i] += count

    def estimate(self, item):
        """Estimate the frequency of the given item."""
        return min(table[i] for table, i in zip(self.table, self.hash_functions(item, self.depth, self.width)))

    def reset(self):
        """Reset the count to the starting state."""
        self.table = np.zeros((self.depth, self.width))
