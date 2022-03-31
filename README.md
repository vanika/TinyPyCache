# TinyPyCache

A feature complete W-TinyLFU cache implementation in Python.

## Description

[W-TinyLFU](https://arxiv.org/pdf/1512.00727.pdf) uses a small admission LRU that evicts to a large Segmented LRU if accepted by the TinyLfu admission policy. TinyLfu relies on a frequency sketch to probabilistically estimate the historic usage of an entry. The window allows the policy to have a high hit rate when entries exhibit recency bursts which would otherwise be rejected. The size of the window vs main space is adaptively determined using a hill climbing optimization. This configuration enables the cache to estimate the frequency and recency of an entry with low overhead.


## Basic Usage

The two main classes is `TinyLFU`. A basic usage example of these may look like so:

__`TinyLFU`__
```python
from tinylfu.tinylfu import TinyLFU

cache = TinyLFU()

def fibonacci(n):
    if n < 2:
        return 1
    if n in cache:
        return cache[n]
    value = fibonacci(n - 1) + fibonacci(n - 2)
    cache[n] = value
    return value
```

## Extended Usage

The cache also provide extra features including statistics monitoring and a decorator use like `functool.lru_cache`.

### Statistics

The cache can be associated with statistics objects, that monitor hits and misses.
First, let's say you only want to record hits and misses for all keys and don't care about any particular key. 
The simplest way to do this is to simply call:

```python
statistics = cache.monitor();
```

This method return a `Statistics` object. It provides methods to get hit and miss rate related to the cache.

```python
statistics.hit_rate() # Cache hit rate
statistics.miss_rate() #  Cache miss rate
statistics.access_for() # Total number of accesses to the cache
```

Note that a hit or miss only refers to lookups (i.e. methods `__contains__(key)`, and `operator[]`) but not insertions.


### Monitoring specific keys

It is also possible to monitor specific keys. Say we were writing a web server accepting HTTP requests and wanted to cache resources  
We're particularly interested in how many cache hits we get for `index.html`, `login.html`, `home.html`. 
For this, it's good to know that the empty `monitor()` call we made further up is actually a method accepting multiple arguments.

Monitor multiple keys.
```python
keys_to_monitor = ["index.html", "login.html", "home.html"]
statistics_keys = cache.monitor(*keys_to_monitor)
values = [cache[v] for v in keys_to_monitor]
result = statistics_keys.hit_rate(*keys_to_monitor)
```

Monitor a single key.
```python
"""Monitor a single key."""
single_key = "index.html"
statistics_single_key = cache.monitor(single_key)
value = cache[single_key]
result = statistics_single_key.hit_rate(single_key)
```

### Function decorator

There is a function that you can use as a decorator to cache the result of your function similar to what 
```@lru_cache```.

```python
    @tinylfu_cache
    def fibonacci(n):
        if n in [1, 2]:
            return 1
        return fibonacci(n - 1) + fibonacci(n - 2)

    print('250th fibonacci number:', fibonacci(250))
```

## References

* http://highscalability.com/blog/2016/1/25/design-of-a-modern-cache.html
* https://github.com/ben-manes/caffeine/wiki
* https://arxiv.org/pdf/1512.00727.pdf
