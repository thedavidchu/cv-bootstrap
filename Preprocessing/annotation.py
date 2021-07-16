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


from shapely import geometry
import numpy as np


class Annotation:
    def __init__(self, image: np.ndarray):
        self.image = np.ndarray
        self.shape = image.shape
        self.store_annotation = {}

        # Information about current annotation
        # If current_annotation is blank, then we add full square!
        self.current_annotation = []

    def add_label(self, label: str):
        # If the current annotation is non-empty
        if self.current_annotation:
            polygon = geometry.Polygon()
            self.store_annotation[label] = self.current_annotation

    def add_point(self, x, y):
        point = geometry.Point(x, y)
        self.current_annotation.append(point)
        return

