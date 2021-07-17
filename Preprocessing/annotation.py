"""
## Notes
1. Only supports single polygon with label.

## User-Interface
___________________________
|                 | LABELS |
|     IMAGE       |        |
|                 |        |
|_________________|________|
|_____MENU________|

### Modes
- Rectangles (2 clicks), Squares (2 click), Rectangles with fixed aspect ratios (2 click)
- Ellipses, Circles, Ellipses with fixed aspect ratio
    - Edge-to-edge (2 clicks) or centre-to-edge (click and drag)
- Draw (rapidly lay points)
- Lines (draw point, line, multiline, polygon, or multipolygon)

### Clicking on the Image
- Left-click and release: drop a point
- Left-click and hold: draw a series of poi

### Clicking on a Point
- Left-click and
- Left-click and hold: drag the point
- Right-click and release: delete point

###

LEFT-CLICK and RELEASE on IMAGE: drop a point
LEFT-CLICK and HOLD on IMAGE: draw a shape (poll frequently)


RIGHT-CLICK and RELEASE on IMAGE: label dropdown

ESC: Escape from current
BACKSPACE: Delete previous point
TAB: Cycle to next labelled part
"""
import shapely.geometry
# from shapely import geometry
import numpy as np
from enum import Enum, auto
import warnings


_UNSAVED_LABEL_WARNING = 'unsaved label. Press ENTER to save or ESC to delete.'


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
    """
    NONE = auto()
    POINT = auto()   # Not supported
    LINE = auto()    # Not supported
    POLYGON = auto()
    CUSTOM = auto()     # Not supported


class LabelMode(Enum):
    BLANK = auto()  # New and blank
    NEW = auto()    # New, needs saving
    VIEW = auto()   # No need to save
    EDIT = auto()   # Exists, but needs saving


class Label:
    """
    A label is a tag/category and a shape/geometry. We will use the
    terms "tag" and "geometry".

    E.g. label = {'dog': Polygon(0 0, 0 10, 10 10, 10 0, 0 0)}

    """
    def __init__(self, lst: list, index: int):
        self.tag = None
        self.geometry = None
        self.mode = LabelMode.BLANK
        self.lst = lst
        self.index = index
        self.points = []

    def is_blank(self):
        return self.mode == LabelMode.BLANK

    def is_unsaved(self):
        """ True if data is unsaved, else False. """
        return (
            self.mode == LabelMode.BLANK
            or self.mode == LabelMode.NEW
            or self.mode == LabelMode.EDIT
        )

    def needs_saving(self):
        return self.mode == LabelMode.NEW or self.mode == LabelMode.EDIT

    def set_unsaved(self):
        """ Sets this label to unsaved. """
        if self.mode == LabelMode.BLANK:
            self.mode = LabelMode.NEW
        elif self.mode == LabelMode.NEW:
            pass
        elif self.mode == LabelMode.VIEW:
            self.mode = LabelMode.EDIT
        elif self.mode == LabelMode.EDIT:
            pass

    def add_tag(self, new_tag: str):
        self.set_unsaved()
        self.tag = new_tag

    def add_xy(self, x, y):
        self.set_unsaved()
        new_point = shapely.geometry.Point(x, y)
        self.points.append(new_point)

    def add_point(self, new_point: shapely.geometry.Point):
        self.set_unsaved()
        self.points.append(new_point)

    def set_geometry(self, geo_mode: GeometryMode):
        self.set_unsaved()

        # First, if nothing selected, label entire picture
        if len(self.points) == 0:
            # TODO(dchu): Call external function to make a box
            raise NotImplementedError('no points chosen. In future, this will select the whole box??? Or pass.')
        elif geo_mode == GeometryMode.NONE:
            pass
        elif len(self.points) == 1:
            self.geometry = self.points[0]
        elif geo_mode == GeometryMode.POINT:
            self.geometry = shapely.geometry.MultiPoint(self.points)
        elif geo_mode == GeometryMode.LINE or len(self.points) == 2:
            self.geometry = shapely.geometry.LineString(self.points)
        elif geo_mode == GeometryMode.POLYGON:
            self.geometry = shapely.geometry.Polygon(self.points)
        return

    def add_geometry(self, geo_mode: GeometryMode):
        self.set_unsaved()

        if self.geometry is None:
            self.set_geometry(geo_mode)
        raise NotImplementedError(
            'GeometryCollections are not yet supported. I am not even '
            'sure if they will be!'
        )
        if geo_mode == GeometryMode.NONE:
            pass
        elif len(self.points) == 1:
            self.geometry = self.points[0]
        elif geo_mode == GeometryMode.POINT:
            self.geometry = shapely.geometry.MultiPoint(self.points)
        elif geo_mode == GeometryMode.LINE or len(self.points) == 2:
            self.geometry = shapely.geometry.LineString(self.points)
        elif geo_mode == GeometryMode.POLYGON:
            self.geometry = shapely.geometry.Polygon(self.points)
        return

    def save(self):
        if self.mode == LabelMode.BLANK:
            return
        elif self.mode == LabelMode.NEW:
            self.lst.insert(self.index, self)
        else:
            self.lst[self.index] = self
        self.mode = LabelMode.VIEW


class ImageLabels:
    def __init__(self, image: np.ndarray):
        self.image = np.ndarray
        self.shape = image.shape
        self.store_labels = []

        # Information about current annotation
        # If current_annotation is blank, then we add full image!
        self.draw_mode = DrawingMode.NONE
        self.geo_mode = GeometryMode.NONE
        self.current_label = Label(self.store_labels, 0)

    def change_draw_mode(self, new_mode: DrawingMode):
        self.draw_mode = new_mode

    def change_geo_mode(self, new_mode: GeometryMode):
        self.geo_mode = new_mode

    def can_change_label(self):
        if self.current_label.needs_saving():
            warnings.warn(_UNSAVED_LABEL_WARNING)
            return False

    def force_reset_label(self):
        self.current_label = Label(self.store_labels, self.current_label.index)

    def new_label(self):
        if self.can_change_label():
            self.current_label = Label(self.store_labels, self.current_label.index + 1)

    def save_label(self):
        self.current_label.save()

    def delete_label(self):
        if self.current_label.is_unsaved():
            self.force_reset_label()
        else:
            self.store_labels.pop(self.current_label.index)
            self.force_reset_label()

    def next_label(self):
        if self.current_label.needs_saving():
            warnings.warn(_UNSAVED_LABEL_WARNING)
            return
        elif len(self.store_labels) == 0:
            return
        next_index = (self.current_label.index + 1) % len(self.store_labels)
        self.current_label = self.store_labels[next_index]

    def prev_label(self):
        if self.current_label.needs_saving():
            warnings.warn(_UNSAVED_LABEL_WARNING)
            return
        elif len(self.store_labels) == 0:
            return
        next_index = (self.current_label.index - 1) % len(self.store_labels)
        self.current_label = self.store_labels[next_index]

    def get_label(self, point: shapely.geometry.Point):
        if not self.can_change_label():
            return
        for label in self.store_labels:
            if point.within(label.geometry):
                self.current_label = label
                return


