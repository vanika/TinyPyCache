from collections import OrderedDict


class Cache:

    def __init__(self, size=128):
        self.size = size
        self.cache = OrderedDict()

    def get(self, key):
        raise NotImplementedError("Please Implement this method")

    def put(self, key, value):
        raise NotImplementedError("Please Implement this method")

    def set(self, key, value):
        raise NotImplementedError("Please Implement this method")

    def __contains__(self, item) -> bool:
        return item in self.cache

    def __len__(self) -> int:
        return len(self.cache)

    def is_full(self) -> bool:
        return len(self.cache) == self.size
