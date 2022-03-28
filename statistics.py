class Statistics:

    """Statistics class used to monitor stats related to a specific cache.
       Args:
           cache: cache to monitor.
           keys: list of keys to monitor.
    Returns:
        Statistics: A Statistics object
    """
    def __init__(self, cache, *keys):
        self.cache = cache
        self.keys = set(keys)
        self.total_access = 0
        self.total_hits = 0

    def hit_rate(self, *keys):
        """Return the hit rate related to the given keys. If keys is empty, return the overall hit rate."""
        if len(self.keys) == 0:
            return 0
        if len(keys) == 0:
            return (self.total_hits / self.total_access) * 100
        else:
            result = dict()
            for key in keys:
                result[key] = self.cache.hit_rate_key(key)
            return result

    def miss_rate(self, *keys):
        """Return the miss rate related to the given keys. If keys is empty, return the overall miss rate."""
        if not keys:
            return (1 - self.total_hits / self.total_access) * 100
        else:
            result = dict()
            for key in keys:
                result[key] = 1 - self.cache.miss_rate_key(key)
            return result

    def access_for(self, keys = None):
        """Return the number of accesses related to the given keys."""
        result = dict()
        for key in keys:
            result[key] = self.cache.access_key(key)

        return result

    def reset(self):
        """Reset the counters to zero."""
        self.total_hits = 0
        self.total_access = 0





