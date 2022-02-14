from typing import List, Type


class CircularBuffer:
    def __init__(self, dtype: Type = None):
        self._dtype: Type = dtype
        self._items: List[dtype] = []
        self._idx: int = 0

        # For iteration
        self._iteration_start: int = None
        self._iteration_idx: int = None

    def __repr__(self):
        return (
            f"({len(self._items)}, {self._dtype}) "
            f"{repr(self._items[self._idx:] + self._items[:self._idx])}"
        )

    def __len__(self):
        return len(self._items)

    @classmethod
    def __class_getitem__(cls, item):
        """Implemented to allow 'CircularBuffer[Type]' to signify this contains
        the Type as the dtype. However, this is just for show. I am unsure of
        how one actually implements this."""
        return cls

    def __getitem__(self, key):
        if not isinstance(key, int):
            return TypeError("key must be an int")
        elif key >= len(self._items):
            raise IndexError("key must be smaller than the number of elements")
        elif key < -len(self._items):
            raise IndexError(
                "key must be greater than or equal to the negative number of "
                "elements"
            )
        return self._items[(self._idx + key) % len(self._items)]

    def __eq__(self, other):
        """Requires other is
            (a) iterable and
            (b) the items of other and self._items implement __eq__().
        This is an O(N^2) algorithm"""
        if len(self._items) != len(other):
            return False
        # Specific case for returning true if both have zero elements because
        # this will pass over the for-loop and go directly to the 'return False'
        # otherwise.
        elif len(self._items) == 0:
            return True
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
        return False

    ####
    #   IDX METHODS
    ####

    def _increment_idx(self, delta: int):
        """Increment the _idx by a certain delta if there is a non-zero
        length."""
        self._idx = (
            (self._idx + delta) % len(self._items)
            if len(self._items)
            else 0
        )

    ####
    #   ITEM METHODS
    ####

    def insert(self, item):
        """Insert an item after the current item and go to the new item."""
        if not isinstance(item, self._dtype):
            raise TypeError(f"Expected type {self._dtype}")
        self._items.insert(self._idx + 1, item)
        self._increment_idx(1)

    def delete(self):
        """Delete the current item and keep the index the same (effectively
        moving to the next)."""
        if not self._items:
            raise ValueError("no more items to delete")
        self._items.pop(self._idx)
        self._idx = self._idx % len(self._items) if len(self._items) else 0

    def get(self):
        """Get current item."""
        if not self._items:
            raise IndexError("items is empty")
        return self._items[self._idx]

    def set(self, item):
        """Set current item."""
        if not isinstance(item, self._dtype):
            raise TypeError(f"Expected type {self._dtype}")
        self._items[self._idx] = item

    ####
    #   NEXT AND PREVIOUS
    ####

    def next(self):
        """Step forward and return that item."""
        if not self._items:
            raise IndexError("items is empty")
        self._increment_idx(1)
        return self._items[self._idx]

    def prev(self):
        """Step backward and return that item."""
        if not self._items:
            raise IndexError("items is empty")
        self._increment_idx(-1)
        return self._items[self._idx]

    ####
    #   EXTERNAL METHODS
    ####

    def to_list(self):
        """Return a self._items, starting at the current index"""
        raise DeprecationWarning("deprecated")
        r = [None] * len(self._items)
        for i, item in enumerate(self._items):
            r[(self._idx + i) % len(self._items)] = item
        return r

    def from_list(self, new_list: List):
        """Fill an empty circular buffer with a new list."""
        # Check that the current list is empty
        if self._items:
            raise ValueError("this object already has items")
        # Check input is a list (a tuple will no suffice, because we will use
        # list methods on this object in other methods.
        if not isinstance(new_list, list):
            raise TypeError("invalid input list")
        # Assert all items are the expected type
        if not all(map(lambda item: isinstance(item, self._dtype), new_list)):
            raise TypeError("not all values are the same type in the list")
        self._items = new_list
        self._idx = 0
