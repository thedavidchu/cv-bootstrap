import tkinter as tk
from PIL import Image, ImageTk
from shapely import geometry as g

from Labelling.backend.images import ImagePaths


class Display:
    def __init__(self, root: tk.Tk):
        self.top_frame = tk.LabelFrame(root)
        self.top_frame.pack(anchor=tk.N, fill='both')
        self.image_frame = tk.LabelFrame(self.top_frame)
        self.image_frame.pack(anchor=tk.NW)
        self.image_canvas = tk.Canvas(master=self.image_frame, width=500, height=500)
        # Packing for above done later
        self.tag_frame = tk.LabelFrame(self.top_frame)
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)

        self.raw_points = []
        self.tk_marks = []
        self.image = None

    def draw_point_and_line(self, event):
        # From https://www.python-course.eu/tkinter_canvas.php
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        if self.raw_points:
            line = self.image_canvas.create_line(event.x, event.y, self.raw_points[-1].x, self.raw_points[-1].y, fill='green')
            self.tk_marks.append(line)
        oval = self.image_canvas.create_oval(x1, y1, x2, y2, fill=python_green)
        self.tk_marks.append(oval)
        self.raw_points.append(g.Point(event.x, event.y))

    def display_next_image(self, image):
        self.image_canvas.pack(side=tk.LEFT, anchor=tk.NW)
        self.image_canvas.bind("<B1-Motion>", self.draw_point_and_line)
        self.image = ImageTk.PhotoImage(image)
        self.image_canvas.create_image(200, 200, anchor=tk.NW, image=self.image)
