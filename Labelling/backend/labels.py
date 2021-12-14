class LabelPaths:
    def __init__(self):
        self._label_paths: list = []
        self._idx: int = 0

    def __len__(self):
        return len(self._label_paths)

    def __getitem__(self, item):
        return self._label_paths[item]

    def __next__(self):
        path = self._label_paths[self._idx]
        self._idx = (self._idx + 1) % len(self._label_paths)
        return path



