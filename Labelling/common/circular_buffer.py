from typing import List


class CircularBuffer:
    def __init__(self, dtype: type):
        self._dtype: type = dtype
        self.items: List[dtype] = []
        self.idx: int = 0

    def __repr__(self):
        return repr(self.items)

    def __len__(self):
        return len(self.items)

    # For iteration
    def __getitem__(self, key):
        return self.items[key]

    def add_item(self, arg):
        self.items.insert(self.idx + 1, arg)

    def get(self):
        """ Get current item. """
        if self.items:
            return self.items[self.idx]
        raise IndexError("items is empty")

    def insert_after_current(self, value):
        """ Insert a value after the current index. Note that this is an O(N) operation. """
        if not isinstance(value, self._dtype):
            raise TypeError(f"Expected type {self._dtype}")
        self.items.insert(self.idx + 1, value)

    def next(self):
        """ Step forward and return that item. """
        if self.items:
            self.idx = (self.idx + 1) % len(self.items)
            return self.items[self.idx]
        raise IndexError("items is empty")

    def prev(self):
        """ Step backward and return that item. """
        if self.items:
            self.idx = (self.idx - 1) % len(self.items)
            return self.items[self.idx]
        raise IndexError("items is empty")
