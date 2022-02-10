from typing import List


class CircularBuffer:
    def __init__(self, dtype: type = None):
        self._dtype: type = dtype
        self._items: List[dtype] = []
        self._idx: int = 0

    def __repr__(self):
        return repr(self._items)

    def __len__(self):
        return len(self._items)

    def __eq__(self, other):
        """Requires other is
            (a) iterable and
            (b) the items of other and self._items implement __eq__().
        This is an O(N^2) algorithm"""
        if len(self._items) != len(other):
            return False
        for i, alignment_item in enumerate(other):
            # Finds where items potentially line up and test all the items if
            # they do line up. We use a generator for (hopefully) early exit
            # if we get an alignment that does not work out.
            if alignment_item == self._items[0] and all(
                item == self._items[(j - i) % len(self._items)]
                for j, item in enumerate(other)
            ):
                return True
            # If one element lines up, but not all the elements are equal in
            # that alignment, it does not imply inequality. This is why we keep
            # searching.
            # E.g. A = [0 1 0 2] vs B = [0 2 0 1]. These two will line up on the
            # first try, but are not equal until the third try.
        else:
            return False

    # For iteration
    def __getitem__(self, key):
        return self._items[key]

    def add_item(self, arg):
        self._items.insert(self._idx + 1, arg)

    def get(self):
        """ Get current item. """
        if self._items:
            return self._items[self._idx]
        raise IndexError("items is empty")

    def to_list(self):
        """Return a self._items, starting at items"""
        r = [None] * len(self._items)
        for i, item in enumerate(self._items):
            r[(self._idx + i) % len(self._items)] = item
        return r

    def from_list(self, new_list):
        self._items = new_list

    def insert_after_current(self, value):
        """ Insert a value after the current index. Note that this is an O(N) operation. """
        if not isinstance(value, self._dtype):
            raise TypeError(f"Expected type {self._dtype}")
        self._items.insert(self._idx + 1, value)

    def delete_current(self):
        """ Delete the current item and keep the index the same (effectively moving to the next)"""
        if self._items:
            self._items.pop(self._idx)
            num = len(self._items)
            self._idx = self._idx % num if num else 0

    def next(self):
        """ Step forward and return that item. """
        if self._items:
            self._idx = (self._idx + 1) % len(self._items)
            return self._items[self._idx]
        raise IndexError("items is empty")

    def prev(self):
        """ Step backward and return that item. """
        if self._items:
            self._idx = (self._idx - 1) % len(self._items)
            return self._items[self._idx]
        raise IndexError("items is empty")
