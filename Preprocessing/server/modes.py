from enum import Enum, auto


class DrawingMode(Enum):
    """
    Define the drawing mode.

    POINTER = 0: On click, select a point or shape
    ONCLICK = 1: On click, drop a point
    CONTINUOUS = 2: On click, continuously lay points
    """
    NONE = auto()
    CLICK = auto()
    DRAG = auto()


class GeometryMode(Enum):
    """
    # Meaning of Modes
    NONE: No mode selected
    POINT: Draw a single point
    LINE: Draw a point in a multi-line
    POLYGON: Draw a point in a polygon (draw holes with right-click mouse)

    ## Notes
    1. Geometry collections are not yet planned to supported.
    2. Custom shapes are not yet planned to be supported
    3. When you edit this, check class::Label and class::ImageLabel.
    """
    NONE = auto()
    POINT = auto()   # Not supported
    LINE = auto()    # Not supported
    POLYGON = auto()
    FULL = auto()
    CUSTOM = auto()     # Not supported


class LabelMode(Enum):
    """
    ## Notes
    1. When you edit this, check class::Label.
    """


    NONE = auto()  # New and blank
    NEW = auto()    # New, needs saving
    EDITED = auto()   # Exists, but needs saving
    SAVED = auto()   # No need to save

