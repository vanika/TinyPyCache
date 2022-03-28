# TinyPyCache

A feature complete W-TinyLFU cache implementation in Python.

## Description

TODO

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

The cache also provide extra features including statistics monitoring, a decorator use like `functool.lru_cache`
and flush to disk.

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


#### Monitoring specific keys

It is also possible to monitor specific keys. Say we were writing a web server accepting HTTP requests and wanted to cache resources 
(I assume that's something people would do). 
Because our website changes in some way every hour, 
we'll use a timed cache with a time-to-live of one hour. 
We're also particularly interested in how many cache hits we get for `index.html`. 
For this, it's good to know that the empty `monitor()` call we made further up is actually a method accepting variadic arguments to forward to the constructor of an 
internal statistics object (the empty `monitor()` calls the default constructor). One
constructor of `Statistics` takes a number of keys to monitor in particular. 
So calling `monitor(key1, key2, ...)` will set up monitoring for those keys. 
We could then something like this:

```python
"""Monitor multiple keys."""
keys_to_monitor = ["index.html", "login.html", "home.html"]
statistics_keys = cache.monitor(*keys_to_monitor)
values = [cache[v] for v in keys_to_monitor]
result = statistics_keys.hit_rate(*keys_to_monitor)

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
