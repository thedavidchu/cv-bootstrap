from enum import Enum
from typing import List, Tuple, Dict, Union
import warnings


class DrawMode(str, Enum):
    NONE = "NONE"
    POINT = "POINT"  # Multiple points
    LINE = "LINE"   # A single, continuous line
    POLYGON = "POLYGON"    # A single, closed polygon
    CONTOUR = "CONTOUR"     # A contour as defined by OpenCV
    SQUARE = "SQUARE"     # A square


class Label:
    """ A label that is written."""
    def __init__(self):
        self.label: Union[str, None] = None     # This is the class
        self.points: List[Tuple[int, int]] = []     # This is the location of the label
        self.marks: List = []   # List of tk marks (not saved)
        self.mode: DrawMode = DrawMode.NONE     # This is the drawing mode

        self.colour: Union[str, None] = None
        self.width: int = 0

    def __bool__(self):
        return self.points != []

    def __repr__(self):
        return f"{self.label}: {self.points}"

    def __eq__(self, other):
        # Check that it is indeed a label
        assert isinstance(other, type(self))
        other: Label = other
        if self.label != other.label:
            return False
        if self.points != other.points:
            return False
        if self.mode != other.mode:
            return False
        if self.width != other.width:
            return False
        # Aesthetics
        if self.colour != other.colour:
            return False
        # NOTE: we skip comparing marks, because the marks may not be loaded and
        # are entirely determined by the points, mode, width, and colour.
        return True

    def add_label(self, label):
        """ Add or modify a label."""
        if self.label is None:
            self.label = label
        else:
            warnings.warn("Overwriting previous label")
            self.label = label

    def set_mode(self, mode: DrawMode):
        self.mode = mode

    def set_width(self, width: int):
        self.width = width

    def set_colour(self, colour: str):
        self.colour = colour

    def dumps(self) -> Dict[str, str]:
        r = None
        if self.mode == DrawMode.NONE:
            warnings.warn("no drawing mode selected")
        elif self.mode in {DrawMode.POINT, DrawMode.LINE, DrawMode.POLYGON}:
            # Convert to lists for JSON (not necessary for storage, but
            # convenient for comparing it to another freshly loaded JSON if we
            # want to check for equality because a tuple and list of the same
            # values do not evaluate as equal).
            r = [list(point) for point in self.points]
        elif self.mode == DrawMode.SQUARE:
            assert len(self.points) == 2
            (x0, y0), (x1, y1) = self.points
            r = [[x0, y0], [x0, y1], [x1, y1], [x1, y0]]
        else:
            raise NotImplementedError("unsupported drawing mode")

        return {
            "category": self.label,
            "geometry": r,
            "mode": self.mode.value,
            "colour": self.colour,
            "width": self.width,
        }

    @classmethod
    def loads(cls, r: dict) -> bool:
        """Load values from a string."""
        result = cls()
        result.label = r.get("category", None)
        if not isinstance(result.label, (str, type(None))):
            result.label = None
            raise TypeError(
                f"label was type {type(result.label)}, expected label to "
                f"either be a string or None"
            )

        result.points = r.get("geometry", [])
        if not isinstance(result.points, list)\
                and all(map(lambda point: isinstance(point, list), result.points))\
                and all(map(lambda point: all(map(lambda x: isinstance(x, int), point))), result.points):
            result.points = []
            raise TypeError(
                "points expected to be a list of list of two integers."
            )
        result.points = [tuple(point) for point in result.points]

        try:
            result.mode = DrawMode[r.get("mode", "NONE")]
        except KeyError:
            result.mode = DrawMode.NONE
            raise TypeError(f"{r.get('mode', 'NONE')} is invalid drawing mode")

        result.colour = r.get("colour", "#00ff00")

        result.width = r.get("width", 1)
        # Error handle width
        return result



