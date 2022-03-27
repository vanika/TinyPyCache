
# -> tinylfu.monitor() -> Statistics object remember that every time you do an
# access the stats obj needs to be updated


class Statistics:

    def __init__(self, cache, keys=None):
        if keys is None:
            keys = []
        self.cache = cache
        self.keys = set(keys)
        self.total_access = 0
        self.total_hits = 0

    def hit_rate(self, *keys):

        if len(self.keys) == 0:
            return 0
        if len(keys) == 0:
            return (self.total_hits / self.total_access) * 100
        else:
            result = dict()
            for key in keys:
                result[key] = self.cache.hit_rate_key(key)
            return result

    def miss_rate(self, keys = None):

        if not keys:
            return (1 - self.total_hits / self.total_access) * 100
        else:
            result = dict()
            for key in keys:
                result[key] = 1 - self.cache.miss_rate_key(key)
            return result

    def access_for(self, keys = None):

        result = dict()
        for key in keys:
            result[key] = self.cache.access_key(key)

        return result

    def reset(self):

        self.total_hits = 0
        self.total_access = 0









