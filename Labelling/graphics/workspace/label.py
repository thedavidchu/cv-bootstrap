from enum import Enum, auto
from typing import List, Tuple, Dict, Union
import warnings

from shapely.geometry import MultiPoint, LineString, Polygon


class DrawMode(Enum):
    NONE = auto()
    POINT = auto()  # Multiple points
    LINE = auto()   # A single, continuous line
    POLYGON = auto()    # A single, closed polygon
    SQUARE = auto()     # A square


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

    def add_label(self, label):
        """ Add or modify a label."""
        if self.label is None:
            self.label = label
        else:
            warnings.warn("Overwriting previous label")
            self.label = label

    def change_mode(self, mode: DrawMode):
        self.mode = mode

    def write(self) -> Dict[str, str]:
        r = None
        if self.mode == DrawMode.NONE:
            warnings.warn("no drawing mode selected")
        elif self.mode == DrawMode.POINT:
            r = MultiPoint(self.points).wkt
        elif self.mode == DrawMode.LINE:
            r = LineString(self.points).wkt
        elif self.mode == DrawMode.POLYGON:
            r = Polygon(self.points).wkt
        elif self.mode == DrawMode.SQUARE:
            assert len(self.points) == 2
            (x0, y0), (x1, y1) = self.points
            r = Polygon(((x0, y0), (x0, y1), (x1, y1), (x1, y0))).wkt
        else:
            raise NotImplementedError("unsupported drawing mode")

        return {
            "category": self.label,
            "geometry": repr(r),
            "colour": self.colour,
            "width": self.width,
        }
