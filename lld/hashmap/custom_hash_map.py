from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class Node(Generic[K, V]):
    key: Optional[K]
    val: Optional[V]
    next: Optional["Node[K, V]"] = None
    prev: Optional["Node[K, V]"] = None


class CustomHashMap(Generic[K, V]):
    def __init__(self) -> None:
        self._INITIAL_SIZE = 4
        self._MAX_CAPACITY = 1 << 30
        self._LOAD_FACTOR = 0.75
        self._count_of_nodes = 0
        self._map: list[Node[K, V]] = [None] * self._INITIAL_SIZE  # type: ignore[list-item]
        for i in range(self._INITIAL_SIZE):
            self._map[i] = Node(None, None)
            self._map[i].next = Node(None, None)
            self._map[i].next.prev = self._map[i]

    def get(self, key: K) -> Optional[V]:
        node = self.find_node(key)
        return None if node is None else node.val

    def put(self, key: K, val: V) -> None:
        node = self.find_node(key)
        if node is not None:
            node.val = val
            return

        bucket = hash(key) % len(self._map)
        head = self._map[bucket]

        new_node = Node(key, val)
        old_first = head.next
        head.next = new_node
        new_node.prev = head
        new_node.next = old_first
        old_first.prev = new_node

        self._count_of_nodes += 1

        if self._count_of_nodes > self._LOAD_FACTOR * len(self._map):
            self._rehash(len(self._map) * 2)

    def remove(self, key: K) -> None:
        node_to_remove = self.find_node(key)

        if node_to_remove is None:
            return

        prev_node = node_to_remove.prev
        next_node = node_to_remove.next

        prev_node.next = next_node
        next_node.prev = prev_node

        self._count_of_nodes -= 1

    def get_size(self) -> int:
        return self._count_of_nodes

    def _rehash(self, new_size: int) -> None:
        if new_size > self._MAX_CAPACITY:
            print("Hashmap is exceeding max capacity")
            return

        new_map: list[Node[K, V]] = [None] * new_size  # type: ignore[list-item]
        for i in range(new_size):
            new_map[i] = Node(None, None)
            new_map[i].next = Node(None, None)
            new_map[i].next.prev = new_map[i]

        for curr in self._map:
            while curr is not None:
                if curr.key is None:
                    curr = curr.next
                    continue

                new_bucket = hash(curr.key) % new_size
                new_head = new_map[new_bucket]
                old_first = new_head.next

                next_node = curr.next

                new_head.next = curr
                curr.prev = new_head
                curr.next = old_first
                old_first.prev = curr

                curr = next_node

        self._map = new_map

    def find_node(self, key: K) -> Optional[Node[K, V]]:
        bucket = hash(key) % len(self._map)
        head = self._map[bucket]

        while head is not None:
            if head.key is not None and head.key == key:
                return head
            head = head.next
        return None
