from enum import Enum, auto
from typing import List, Tuple
import warnings

from shapely.geometry import MultiPoint, LineString, Polygon


class DrawMode(Enum):
    NONE = auto()
    POINT = auto()  # Multiple points
    LINE = auto()   # A single, continuous line
    POLYGON = auto()    # A single, closed polygon
    SQUARE = auto()     # A square


class Label:
    """ A label that is written. """
    def __init__(self):
        self.label: str
        self.points: List[Tuple[int, int]] = []
        self.marks: List = []   # List of tk marks
        self.mode: DrawMode = DrawMode.NONE

    def change_mode(self, mode: DrawMode):
        self.mode = mode

    def write(self) -> str:
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
        return repr(r)
