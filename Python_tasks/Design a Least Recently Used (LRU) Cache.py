class _Node:
    """Doubly linked list node holding a key/value pair."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be a positive integer")

        self.capacity = capacity
        self.cache = {}  # key -> _Node, gives O(1) lookup

        # Sentinel head/tail nodes simplify edge cases (empty list, single node)
        # head.next is the MOST recently used node
        # tail.prev is the LEAST recently used node
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- internal doubly linked list helpers (all O(1)) ---

    def _remove(self, node):
        """Unlink a node from its current position."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_front(self, node):
        """Insert a node right after head (marks it as most recently used)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node):
        self._remove(node)
        self._insert_at_front(node)

    # --- public API ---

    def get(self, key):
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_front(node)  # accessing counts as using
        return node.value

    def put(self, key, value):
        if key in self.cache:
            # Update existing entry; no eviction needed
            node = self.cache[key]
            node.value = value
            self._move_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            # Evict least recently used: the node just before tail
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

        new_node = _Node(key, value)
        self.cache[key] = new_node
        self._insert_at_front(new_node)

    def peek_order(self):
        """Return keys from most recently used to least recently used."""
        order = []
        current = self.head.next
        while current is not self.tail:
            order.append(current.key)
            current = current.next
        return order


# --- Sample run ---
if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, "A")
    cache.put(2, "B")
    print(cache.get(1))        # "A" — 1 is now most recent
    cache.put(3, "C")          # evicts 2 (least recently used)
    print(cache.get(2))        # -1 (evicted)
    cache.put(4, "D")          # evicts 1 (now least recently used)
    print(cache.get(1))        # -1 (evicted)
    print(cache.get(3))        # "C"
    print(cache.get(4))        # "D"
    print(cache.peek_order())  # [4, 3]