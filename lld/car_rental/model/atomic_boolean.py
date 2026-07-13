import threading


class AtomicBoolean:
    def __init__(self, initial: bool = False) -> None:
        self._value = initial
        self._lock = threading.Lock()

    def get(self) -> bool:
        return self._value

    def set(self, value: bool) -> None:
        with self._lock:
            self._value = value

    def compare_and_set(self, expect: bool, update: bool) -> bool:
        with self._lock:
            if self._value == expect:
                self._value = update
                return True
            return False
