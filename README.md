# TinyPyCache

TinyPyCache is a Python server which is used to expose a tinyLFU 
in-memory cache and operations over it to networked clients. 
It uses a simple ASCII protocol which is human readable.

Window TinyLFU (W-TinyLFU) uses the sketch as a filter, 
admitting a new entry if it has a higher frequency than 
the entry that would have to be evicted to make room for it. 
Instead of filtering immediately, an admission window gives an entry 
a chance to build up its popularity. This avoids consecutive misses, especially in cases
like sparse bursts where an entry may not be deemed suitable for long-term retention. 
To keep the history fresh an aging process is performed periodically or incrementally 
to halve all of the counters.

## Network protocol

### Get 

```
GET <<key>> 
```

### Add

```
GET <<key>> && <<value>>
```