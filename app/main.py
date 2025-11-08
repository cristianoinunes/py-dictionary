from typing import Any, List, Tuple


class Dictionary:
    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity: int = initial_capacity
        self._size: int = 0
        self._load_factor: float = 0.75
        self._buckets: List[List[Tuple[Any, int, Any]]] = [
            [] for _ in range(self._capacity)
        ]

    def __len__(self) -> int:
        return self._size

    def __setitem__(self, key: Any, value: Any) -> None:
        h: int = hash(key)
        index: int = h % self._capacity
        bucket: List[Tuple[Any, int, Any]] = self._buckets[index]

        for i, (k, khash, v) in enumerate(bucket):
            if khash == h and k == key:
                bucket[i] = (key, h, value)
                return

        bucket.append((key, h, value))
        self._size += 1

        if self._size / self._capacity > self._load_factor:
            self._resize()

    def __getitem__(self, key: Any) -> Any:
        h: int = hash(key)
        index: int = h % self._capacity
        bucket: List[Tuple[Any, int, Any]] = self._buckets[index]

        for k, khash, v in bucket:
            if khash == h and k == key:
                return v
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        h: int = hash(key)
        index: int = h % self._capacity
        bucket: List[Tuple[Any, int, Any]] = self._buckets[index]

        for i, (k, khash, v) in enumerate(bucket):
            if khash == h and k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def _resize(self) -> None:
        old_buckets: List[List[Tuple[Any, int, Any]]] = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        old_size: int = self._size
        self._size = 0

        for bucket in old_buckets:
            for k, h, v in bucket:
                index: int = h % self._capacity
                self._buckets[index].append((k, h, v))
                self._size += 1

        assert self._size == old_size
