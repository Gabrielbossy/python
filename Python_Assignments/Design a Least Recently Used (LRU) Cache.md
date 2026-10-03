The Problem: Design a Least Recently Used (LRU) Cache

Background:
You're building a caching layer for a product API that serves frequently requested item lookups. Since memory is limited, the cache can only hold a fixed number of items. When it's full and a new item needs to be cached, the least recently used item should be evicted to make room. Accessing an item (via get) counts as "using" it, so it becomes the most recently used.

This is a classic data structure design problem, not a batch-processing script — you're building a class with stateful methods that get called repeatedly over time.

The Requirements:

1. Class & Architecture
Implement a class called LRUCache.

__init__(self, capacity): initializes the cache with a fixed positive integer capacity. Raise ValueError if capacity <= 0.
get(self, key): returns the value associated with key if it exists, else returns -1. A successful get must mark that key as most recently used.
put(self, key, value): inserts or updates the value for key. If inserting a new key would exceed capacity, evict the least recently used key first. If key already exists, update its value and mark it as most recently used.

2. Performance Constraint
Both get and put must run in O(1) average time complexity. This rules out a naive approach like scanning a list to find the oldest item — you need a data structure combination that gives O(1) lookup and O(1) reordering.

(Hint: Python's OrderedDict or a combination of a dict + a doubly linked list both satisfy this. Implement it with a doubly linked list + dict to demonstrate the underlying mechanics, rather than relying on OrderedDict's built-in move_to_end.)

3. Edge Cases to Handle

Calling get on a key that was evicted or never existed → return -1, don't raise.
Calling put on a key that already exists → update its value, refresh its recency, and do not evict anything (it's not a new entry).
capacity == 1 → every put of a new key evicts the sole existing entry.

4. Observability
Add a method peek_order(self) that returns a list of all keys currently in the cache, ordered from most recently used to least recently used — useful for testing and debugging without affecting recency.

Sample Test Sequence

python
cache = LRUCache(2)
cache.put(1, "A")       # cache: {1: A}
cache.put(2, "B")       # cache: {1: A, 2: B}
print(cache.get(1))     # returns "A", 1 is now most recent
cache.put(3, "C")       # capacity exceeded -> evicts 2 (least recently used)
print(cache.get(2))     # returns -1 (evicted)
cache.put(4, "D")       # evicts 1 (now least recently used)
print(cache.get(1))     # returns -1 (evicted)
print(cache.get(3))     # returns "C"
print(cache.get(4))     # returns "D"
print(cache.peek_order())  # expect [4, 3] (most recent first)