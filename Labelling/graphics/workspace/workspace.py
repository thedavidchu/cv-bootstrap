import tkinter as tk
from PIL import Image, ImageTk

import shapely.geometry as g


class WorkSpace:
    def __init__(self, app):
        self.app = app

        self.workspace_frame = tk.LabelFrame(app.root)
        self.workspace_frame.pack(anchor=tk.N, fill="both")

        self.image_frame = tk.LabelFrame(self.workspace_frame)
        self.image_frame.pack(anchor=tk.NW, fill="both")

        self.canvas_frame = None
        # Packing for above done later

        self.tag_frame = tk.LabelFrame(self.workspace_frame)
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)

        self.points = []    # List of points
        self.tk_marks = []  # List of tk marks in order (for undo)
        self.point_colour = "#476042"
        self.line_colour = "green"
        self.image = None

    def draw_point_and_line(self, event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        # If previous point exists, add line
        if self.points:
            line = self.canvas_frame.create_line(
                event.x,
                event.y,
                self.points[-1].x,
                self.points[-1].y,
                fill=self.line_colour
            )
            self.tk_marks.append(line)

        # Draw point
        point = self.canvas_frame.create_oval(x1, y1, x2, y2, fill=self.point_colour)
        self.tk_marks.append(point)
        self.points.append(g.Point(event.x, event.y))

    def connect_ends(self, event=None):
        if len(self.points) >= 2:
            first_point, last_point = self.points[0], self.points[-1]
            line = self.canvas_frame.create_line(
                first_point.x, first_point.y,
                last_point.x, last_point.y,
                fill=self.line_colour
            )
            self.tk_marks.append(line)
        else:
            print("Blah")
        # TODO save shape into IR

    def delete_last_point(self, event=None):
        print("BackSpace")
        if len(self.points):
            self.points.pop()
        if len(self.tk_marks):
            point = self.tk_marks.pop()
            self.tk_marks.pop()

    def display_image(self, image: Image):
        width, height = image.size

        self.canvas_frame = tk.Canvas(master=self.image_frame, width=width, height=height)
        self.canvas_frame.pack(side=tk.LEFT, anchor=tk.NW)
        self.canvas_frame.bind("<Button-1>", self.draw_point_and_line)
        self.canvas_frame.bind("<B1-Motion>", self.draw_point_and_line)

        self.canvas_frame.bind("<Return>", self.connect_ends)
        self.canvas_frame.bind("<BackSpace>", self.delete_last_point)

        # Attach image
        self.image = ImageTk.PhotoImage(image)
        self.canvas_frame.create_image(0, 0, anchor=tk.NW, image=self.image)
