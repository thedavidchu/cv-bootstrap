"""
TODO(dchu):
* Return polynomial coefficients
* Threshold groups of rectangles by size
* Split really wide (i.e. poorly fit) rectangles...
    * Figure out threshold and method
"""

import json

import cv2
import numpy as np
from shapely.geometry import Polygon

RED = (0, 0, 255)
ORANGE = (0, 127, 255)
YELLOW = (0, 255, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
COLOURS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE] + [GREY] * 1000

LABEL_PATH = (
    r"C:\Users\theda\PycharmProjects\cv-bootstrap\data"
    r"\Night Time Dashcam_5..9_labels\Night Time Dashcam_9_labels"
    r"\Lane_Input_5450.json"
)
SEGMENT_PATH = "./segmented_label.jpg"


def gen_segmented(obj: dict) -> np.ndarray:
    height, width = obj["image_size"]
    depth = 3
    img = np.zeros(shape=(height, width, depth), dtype=np.uint8)
    for label in obj["labels"]:
        # So far, we only support polygons <3
        if label["mode"] != "POLYGON":
            raise NotImplementedError("only polygons supported")
        points = np.array(label["geometry"], dtype=np.int32).reshape((-1, 1, 2))
        # For some reason, the points need to be wrapped in a list.
        cv2.polylines(
            img=img, pts=[points], isClosed=True,
            color=WHITE, thickness=max([1, label["width"]])
            )
        cv2.fillPoly(img, [points], WHITE)
    return img


def bound_contours(contours: list):
    r = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        r.append(box)
    return r


def stretch_rectangle(rect: np.ndarray, scale: float = 1.3) -> np.ndarray:
    # 1. Find longest side
    p0, p1, p2, p3 = rect

    centre = np.mean([p0, p1, p2, p3], axis=0)

    v0_1 = p0 - p1
    v1_2 = p1 - p2
    v2_3 = p2 - p3  # == -dir0_1
    v3_0 = p3 - p0  # == -dir1_2

    avg_v_a = np.mean([v0_1, -v2_3], axis=0)
    avg_v_b = np.mean([v1_2, -v3_0], axis=0)

    # 2. Find slope of longest side
    shorter, longer = sorted([avg_v_a, avg_v_b], key=np.linalg.norm)

    # 3. Stretch by adding along longer dimension
    return np.array([
        centre + 1 / 2 * shorter + scale / 2 * longer,
        centre - 1 / 2 * shorter + scale / 2 * longer,
        centre - 1 / 2 * shorter - scale / 2 * longer,
        centre + 1 / 2 * shorter - scale / 2 * longer,
    ])


def find_overlap_original(bounding_boxes, extended_boxes):
    # 1. Find new boxes that overlap with original boxes
    assert len(bounding_boxes) == len(extended_boxes)
    length = len(bounding_boxes)
    overlap = [[None for j in range(length)] for i in range(length)]

    polygon_bounding_boxes = [Polygon(box) for box in bounding_boxes]
    polygon_extended_boxes = [Polygon(box) for box in extended_boxes]
    for i, extended_box in enumerate(polygon_extended_boxes):
        for j, bounding_box in enumerate(polygon_bounding_boxes):
            if i == j:
                overlap[i][j] = True
            overlap[i][j] = extended_box.intersects(bounding_box)

    # 2. Find all of the descendants
    graph = {
        # Map node to its immediate descendants
        i: {
            j for j, is_overlap in enumerate(row) if is_overlap
        } for i, row in enumerate(overlap)
    }

    def get_all_descendants(graph, root, unvisited):
        """Get all the descendants of a root recursively, include itself."""
        descendants = {root}    # Include root in list of descendants
        unvisited -= {root}
        for child in graph[root]:
            if child not in unvisited:
                continue
            # Remove the current from unmatched so we do not cycle
            unvisited -= {child}
            # We rely on the side-effects to reduce the size of unvisited
            descendants.update({child})
            descendants.update(get_all_descendants(graph, child, unvisited))
        return descendants

    for root in graph.keys():
        # Updating the graph like this makes the recursion flatter?
        graph[root] = get_all_descendants(graph, root, set(graph.keys()))

    # Make the graph a bidirectional graph (so a child will list its parents)
    for root in graph.keys():
        for child in graph[root]:
            graph[child].update({root})

    # 3. Group all these boxes into families
    families = []
    for root in graph.keys():
        if graph[root] not in families:
            families.append(graph[root])

    # 4. Return the original boxes grouped by family
    r = []
    for f in families:
        r.append([bounding_boxes[i] for i in f])
    return r


def draw_boxes(img: np.ndarray, boxes, title="Bounded Labels", colour=GREY):
    for box in boxes:
        box = stretch_rectangle(box, scale=1.3)
        box = np.int0(box)  # Cast to long int?
        cv2.drawContours(img, [box], 0, colour, 2)
    cv2.imshow(title, img)


def draw_lines(img: np.ndarray, x_arr, y_arr, title="Lines", colour=GREY):
    points = list(zip(x_arr, y_arr))
    for p0, p1 in zip(points[:-1], points[1:]):
        p0_, p1_ = np.array(p0, dtype=int), np.array(p1, dtype=int)
        cv2.line(img, p0_, p1_, color=colour, thickness=3)
    cv2.imshow(title, img)


if __name__ == "__main__":
    # Get segmented labels
    with open(LABEL_PATH) as f:
        label = json.load(f)
    img = gen_segmented(label)
    # Draw segmented labels
    cv2.imshow('1 - Segmentation', img)

    # Get contours
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
    # Draw contours
    img_cp = img.copy()
    cv2.drawContours(img_cp, contours, -1, (0, 255, 0), 3)
    cv2.imshow('2 - Contours', img_cp)

    bounding_boxes = bound_contours(contours)
    img_cp = img.copy()
    draw_boxes(img_cp, bounding_boxes, title="3 - Bound Boxes")
    extended_boxes = [stretch_rectangle(box, scale=1.3) for box in bounding_boxes]
    img_cp = img.copy()
    draw_boxes(img_cp, extended_boxes, title="4 - Extended Boxes")

    families = find_overlap_original(bounding_boxes, extended_boxes)
    img_cp = img.copy()
    for i, f in enumerate(families):
        draw_boxes(img_cp, f, title="5 - Families", colour=COLOURS[i])

    # For each family, run a linear fit (quadratic fit doesn't work bc we only use end points)
    clusters = [np.concatenate(f) for f in families]
    polynomial_approximations = [np.poly1d(np.polyfit(x=c[:, 0], y=c[:, 1], deg=1)) for c in clusters]
    img_cp = img.copy()
    for i, poly in enumerate(polynomial_approximations):
        x = np.linspace(1, 1280)
        y = poly(x)
        draw_lines(img_cp, x, y, "6 - Polynomial Approximations", colour=COLOURS[i])

    cv2.waitKey(0)
    cv2.destroyAllWindows()