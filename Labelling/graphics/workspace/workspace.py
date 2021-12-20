import tkinter as tk
from PIL import Image, ImageTk

import warnings

import shapely.geometry as g

from Labelling.common.circular_buffer import CircularBuffer
from Labelling.graphics.common import unimplemented_fnc1
from Labelling.graphics.workspace.label import DrawMode, Label


class WorkSpace:
    def __init__(self, app):
        self.app = app

        self.workspace_frame = tk.LabelFrame(app.root)
        self.workspace_frame.pack(anchor=tk.N, fill="both")

        self.image_frame = tk.LabelFrame(self.workspace_frame)
        self.image_frame.pack(anchor=tk.NW)

        self.canvas_frame = None
        # Packing for above done later

        self.tag_frame = tk.LabelFrame(self.workspace_frame)
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)

        self.mode: DrawMode = DrawMode.LINE     # Store previous mode
        self.labels = CircularBuffer(Label)
        self.labels.add_item(Label())
        self.labels.get().mode = self.mode  # Initialize mode (default to NONE in deployment)

        self.buffer = []    # List of chars
        self.point_colour = "#476042"
        self.line_colour = "green"
        self.image = None

    def config_keyboard(self):
        self.canvas_frame.focus_set()   # Needed to recognize keyboard commands

        # Control keys
        self.canvas_frame.bind("<Return>", unimplemented_fnc1)
        self.canvas_frame.bind("<BackSpace>", unimplemented_fnc1)
        # self.canvas_frame.bind("<>", unimplemented_fnc1)
        # self.canvas_frame.bind("<>", unimplemented_fnc1)
        # self.canvas_frame.bind("<>", unimplemented_fnc1)
        # self.canvas_frame.bind("<>", unimplemented_fnc1)
        # self.canvas_frame.bind("<>", unimplemented_fnc1)

        alpha = r"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        for char in alpha:
            self.canvas_frame.bind(f"<{char}>", lambda x: print(self.buffer))

    def draw(self, event):
        x, y = event.x, event.y

        current_label: Label = self.labels.get()
        self.mode = current_label.mode
        points = current_label.points
        prev_x, prev_y = points[-1] if points else (None, None)
        points.append((x, y))

        mode = current_label.mode
        if mode == DrawMode.NONE:
            warnings.warn("no drawing mode selected")
            return
        elif mode == DrawMode.SQUARE:
            raise NotImplementedError("squares are not yet supported")
        if mode == DrawMode.POINT:
            pass
        elif mode == DrawMode.LINE or mode == DrawMode.POLYGON:
            if len(points) >= 2:
                line = self.canvas_frame.create_line(
                    x,
                    y,
                    prev_x,
                    prev_y,
                    fill=self.line_colour
                )
                current_label.marks.append(line)
        else:
            raise NotImplementedError("unsupported drawing mode")
        point_mark = self.canvas_frame.create_oval(x - 1, y - 1, x + 1, y + 1, fill=self.point_colour)
        current_label.marks.append(point_mark)

    def write(self, event=None):
        """ Write current label to console. Switch to next label. """
        current_label: Label = self.labels.get()
        self.mode = current_label.mode  # Carry mode over to next

        if current_label.mode == DrawMode.POLYGON and len(current_label.points) >= 2:
            x, y = current_label.points[0]
            self.draw(g.Point(x, y))
        print(current_label.write())
        self.labels.add_item(Label())
        self.labels.next()
        self.labels.get().mode = self.mode

    def to_json(self, event=None):
        r = {}
        for i, label in enumerate(self.labels):
            r[f"{i}"] = label.write()

        print(r)
        return r

    def display_image(self, image: Image):
        width, height = image.size

        self.canvas_frame = tk.Canvas(master=self.image_frame, width=width, height=height)
        self.canvas_frame.pack(side=tk.LEFT, anchor=tk.NW)
        self.canvas_frame.bind("<Button-1>", self.draw)
        self.canvas_frame.bind("<B1-Motion>", self.draw)

        self.canvas_frame.focus_set()   # Needed to recognize keyboard commands
        self.canvas_frame.bind("<Return>", self.write)
        self.canvas_frame.bind("<Control-s>", self.to_json)
        self.canvas_frame.bind("<Control-z>", unimplemented_fnc1)

        # Attach image
        self.image = ImageTk.PhotoImage(image)
        self.canvas_frame.create_image(0, 0, anchor=tk.NW, image=self.image)
