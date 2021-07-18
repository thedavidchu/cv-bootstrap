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
from Preprocessing.server.modes import DrawingMode, GeometryMode, LabelMode
import numpy as np
import warnings


_UNSAVED_LABEL_WARNING = 'unsaved label. Press ENTER to save or ESC ' \
                         'to delete. Actually, this is entirely ' \
                         'dependent on the UI. Currently, it is not' \
                         'implemented.'


class Label:
    """
    A label is a tag/category and a shape/geometry. We will use the
    terms "tag" and "geometry".

    E.g. label = {'dog': Polygon(0 0, 0 10, 10 10, 10 0, 0 0)}

    A Label object is a deterministic finite-state machine. The states
    are:
    1. NONE - new and unmodified
    2. NEW - new and modified
    2. EDITED - indexed but there are unsaved changes
    3. SAVED - saved and indexed

    """
    def __init__(self, lst: list, index: int, shape: tuple):
        # Return values
        self.tag = None
        self.geometry = None

        # Indexing into list to save
        self.mode = LabelMode.NONE
        self.lst = lst
        self.index = index

        # List of points (using matrix-coordinate system)
        self.points = []
        self.image_shape = shapely.geometry.box(
            0, 0, shape[0], shape[1]
        )

    # ==================== GET CONDITIONS ==================== #
    def is_unsaved(self):
        """ True if it contains unsaved data. """
        return self.mode in {
            LabelMode.NONE,
            LabelMode.NEW,
            LabelMode.EDITED,
        }

    def is_unindexed(self):
        return self.mode in {
            LabelMode.NONE,
            LabelMode.NEW,
        }

    def need_save(self):
        return self.mode in {
            LabelMode.NEW,
            LabelMode.EDITED
        }

    def __set_saved(self):
        self.mode = LabelMode.SAVED

    def __set_need_save(self):
        """ Sets this label to unsaved. """
        if self.need_save():
            pass
        elif self.is_unindexed():
            self.mode = LabelMode.NEW
        else:
            self.mode = LabelMode.EDITED

    # ==================== NONE -> NEW; SAVED -> EDITED ==================== #
    def add_tag(self, new_tag: str):
        self.__set_unsaved()
        self.tag = new_tag

    def add_point(
            self,
            x: (shapely.geometry.Point, int, float),
            y: (int, float) = None
    ):
        self.__set_unsaved()
        if isinstance(x, shapely.geometry.Point) and y is None:
            new_point = x
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)):
            new_point = shapely.geometry.Point(x, y)
        else:
            raise TypeError('inputs must be a single point or two numerics')

        if new_point.within(self.image_shape):
            self.points.append(new_point)
        else:
            raise ValueError('input point must be within the image!')

    # ==================== NEW, EDITED -> SAVED ==================== #
    def __set_geometry(self, geo_mode: GeometryMode):
        """
        ## Notes
        1. GeometryCollections are not supported (this feature may be
            too broad).
        2. Adding to a geometry collection is not yet supported (this
            is an important feature to be able to edit previous labels
            and shall be implemented in the future).
        """
        # First, check if label entire picture
        if geo_mode == GeometryMode.FULL:
            warnings.warn(
                'I have not tested the bounds of the shape.'
            )
            self.geometry = self.image_shape
        # If no labels, error out
        elif len(self.points) == 0:
            # TODO(dchu): Call external function to make a box
            raise NotImplementedError(
                'no points chosen. In future, this will either select '
                'the entire box or will do nothing. This is a design '
                'decision between convenience (the former) and '
                'intuitive/fail-safe design (the latte). If we wish '
                'to label an entire box, this should be the default, '
                'but also explicitly stated.'
            )
        elif geo_mode == GeometryMode.NONE:
            warnings.warn(
                'no geometry selected. This action does nothing'
            )
        elif len(self.points) == 1:
            self.geometry = self.points[0]
        elif geo_mode == GeometryMode.POINT:
            self.geometry = shapely.geometry.MultiPoint(self.points)
        elif geo_mode == GeometryMode.LINE or len(self.points) == 2:
            self.geometry = shapely.geometry.LineString(self.points)
        elif geo_mode == GeometryMode.POLYGON:
            self.geometry = shapely.geometry.Polygon(self.points)
        else:
            raise NotImplementedError(
                'currently unsupported geometry type.'
            )
        return

    def save(self, geo_mode: GeometryMode):
        # NONE and SAVED needn't be saved
        if not self.need_save():
            return
        # NEW needs to be indexed
        elif self.is_unindexed():
            self.lst.insert(self.index, self)
        self.__set_saved()
        self.__set_geometry(geo_mode)

    # ==================== NEW, EDITED, SAVED -> NONE ==================== #
    def reset(self, index: int = None):
        self.tag = None
        self.geometry = None
        self.mode = LabelMode.NONE
        self.index = index if index is not None else self.index
        self.points = []

    def delete(self):
        self.lst.pop(self.index)


class ImageLabels:
    def __init__(self, image_shape: tuple):
        """
        # Notes
        1. Assumes a rectangular image with height and width
            dimensions.
        2. Channel dimension is optional.
        """
        # Image properties
        self.shape = image_shape

        # List of all labels
        self.store_labels = []

        # Modes
        self.draw_mode = DrawingMode.NONE
        self.geo_mode = GeometryMode.NONE

        # Information about current label
        self.current_label = Label(self.store_labels, 0, self.shape)

    # ==================== CONDITIONS ==================== #
    def is_empty(self):
        return not self.store_labels

    # ==================== CHANGE MODES ==================== #
    def change_draw_mode(self, new_mode: DrawingMode):
        self.draw_mode = new_mode

    def change_geo_mode(self, new_mode: GeometryMode):
        self.geo_mode = new_mode

    # ==================== LABELING ==================== #
    def add_label_tag(self, new_tag: str):
        self.current_label.add_tag(new_tag)

    def add_label_point(
        self,
        x: (shapely.geometry.Point, int, float),
        y: (int, float) = None
    ):
        # Error messaging will be down the stack
        self.current_label.add_point(x, y)

    # ==================== LABEL MANIPULATION ==================== #
    def __can_change_label(self):
        return not self.current_label.need_save()

    def new_label(self):
        if self.__can_change_label():
            self.current_label.reset(self.current_label.index + 1)
        else:
            warnings.warn(_UNSAVED_LABEL_WARNING)

    def save_label(self):
        self.current_label.save()

    def delete_label(self):
        if not self.current_label.is_unindexed():
            self.current_label.delete()
        self.current_label.reset()

    def next_store_label(self):
        if not self.__can_change_label():
            warnings.warn(_UNSAVED_LABEL_WARNING)
            return
        elif self.is_empty():
            return
        else:
            next_index = (self.current_label.index + 1) % len(self.store_labels)
            self.current_label = self.store_labels[next_index]

    def prev_store_label(self):
        if not self.__can_change_label():
            warnings.warn(_UNSAVED_LABEL_WARNING)
            return
        elif self.is_empty():
            return
        else:
            next_index = (self.current_label.index - 1) % len(self.store_labels)
            self.current_label = self.store_labels[next_index]

    def get_label(self, point: shapely.geometry.Point):
        if not self.can_change_label():
            return
        for label in self.store_labels:
            if point.within(label.geometry):
                self.current_label = label
                return
