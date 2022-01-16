import os.path
import tkinter as tk
import json
from PIL import Image, ImageTk

import warnings

import shapely.geometry as g

from Labelling.common.circular_buffer import CircularBuffer
from Labelling.config.constants import TEST_LABEL_DIR_PATH
from Labelling.graphics.common import unimplemented_fnc1
from Labelling.graphics.workspace.label import DrawMode, Label


class WorkSpace:
    """
    ## Keyboard Commands
    Tab - Save and switch to next existing
    Shift + Tab - Save and switch to previous existing
    Return - Save and create a new label as the next label

    """
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
        self.labels: CircularBuffer[Label] = CircularBuffer(Label)
        self.labels.add_item(Label())
        self.labels.get().mode = self.mode  # Initialize mode (default to NONE in deployment)

        self.buffer = []    # List of chars
        self.point_colour = "green"
        self.background_line_colour = "green"
        self.focus_line_colour = "red"
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

    def change_mode(self, new_mode: DrawMode):
        self.mode = new_mode
        self.labels.get().change_mode(new_mode)
        if new_mode != DrawMode.NONE:
            print("Replacing marks")
            self.replace_marks(self.focus_line_colour)    # Redraw line in "focus" colour

    # ==================== MARKS AND POINTS ==================== #
    def draw(self, event=None, line_colour=None):
        """Draw points on the screen and write points to labels."""
        x, y = event.x, event.y
        line_colour = self.focus_line_colour if line_colour is None else line_colour

        current_label: Label = self.labels.get()
        self.mode = current_label.mode  # Set mode to current label's mode
        points = current_label.points
        prev_x, prev_y = points[-1] if points else (None, None)
        points.append((x, y))   # Add point to label's list of points (spooky action at a distance)

        mode = current_label.mode   # TODO - Better in match-case statement
        width = self.app.bottom_tool_bar.line_width.get()
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
                    fill=line_colour,
                    width=width,
                )
                current_label.marks.append(line)
        else:
            raise NotImplementedError("unsupported drawing mode")
        r = max(1, width // 2)
        point_mark = self.canvas_frame.create_oval(x - r, y - r, x + r, y + r, fill=self.point_colour)
        current_label.marks.append(point_mark)

    def erase(self, event=None):
        """ Erase drawing marks and points. """
        current_label: Label = self.labels.get()
        if len(current_label.marks) == len(current_label.points) == 0:
            # Nothing to delete
            pass
        elif len(current_label.marks) == 1 and len(current_label.points) == 1:
            self.canvas_frame.delete(current_label.marks.pop(-1))
            current_label.points.pop(-1)
        elif current_label.mode == DrawMode.POINT:
            # We know that there is at least 1 point, so this is valid
            # This is a separate case because these points won't be joined by a line
            self.canvas_frame.delete(current_label.marks.pop(-1))
            current_label.points.pop(-1)
        else:
            self.canvas_frame.delete(current_label.marks.pop(-1))
            self.canvas_frame.delete(current_label.marks.pop(-1))
            current_label.points.pop(-1)

    def replace_marks(self, line_colour=None, blah=None):
        """ Replace an on-screen annotation with a different colour in the same mode. """
        line_colour = self.background_line_colour if line_colour is None else line_colour
        current_label: Label = self.labels.get()

        marks = current_label.marks
        points = current_label.points

        current_label.marks = []
        current_label.points = []
        # Delete markings from canvas and from scope
        for mark in marks:
            self.canvas_frame.delete(mark)
        # Redraw points
        for point in points:
            self.draw(g.Point(*point), line_colour=line_colour)

    # ==================== WHICH LABELS ==================== #
    # Just completes polygons, doesn't actually do any writing
    def write_to_label(self):
        """ Writes to label. NOTE - this doesn't actually happen here. It happens in draw. """
        current_label: Label = self.labels.get()
        # Complete Polygon if applicable
        if current_label.mode == DrawMode.POLYGON and len(current_label.points) >= 2:
            x, y = current_label.points[0]
            self.draw(g.Point(x, y))
        print(current_label)

    def goto_next_label(self, event=None):
        """ Advance to the next label without saving to file. """
        self.write_to_label()
        self.replace_marks(self.background_line_colour)    # Redraw line in "background" colour
        self.labels.next()
        self.replace_marks(self.focus_line_colour)  # Redraw line in "focus" colour
        self.change_mode(self.labels.get().mode)    # Also redraws line (redundantly)

    def goto_prev_label(self, event=None):
        """ Go to the previous label without saving to file. """
        self.write_to_label()
        self.replace_marks(self.background_line_colour)    # Redraw line in "background" colour
        self.labels.prev()
        self.replace_marks(self.focus_line_colour)  # Redraw line in "focus" colour
        self.change_mode(self.labels.get().mode)  # Also redraws line (redundantly)

    def goto_new_label(self, event=None):
        """ Go to the next, newly created label unless the current label has no points. """
        if self.labels.get().points:
            draw_mode = self.labels.get().mode
            self.write_to_label()
            self.replace_marks(self.background_line_colour)  # Redraw line in "background" colour
            # Create new label and switch to it
            self.labels.insert_after_current(Label())
            self.labels.next()
            # Set draw mode the same as previously
            self.labels.get().mode = draw_mode
            self.replace_marks(self.focus_line_colour)  # Redraw line in "focus" colour
            self.change_mode(self.labels.get().mode)  # Also redraws line (redundantly)
        else:
            # Empty label, so don't write
            pass

    # ==================== SAVING ==================== #
    def save(self, event=None):
        """ Save all labels. """
        self.write_to_label()
        r = {repr(i): label.write() for i, label in enumerate(self.labels)}
        label_path: str = self.app.image_paths.get_label_path()
        with open(label_path, "w") as f:
            json.dump(obj=r, fp=f, indent=4)

    def display_image(self, image: Image):
        width, height = image.size

        self.canvas_frame = tk.Canvas(master=self.image_frame, width=width, height=height)
        self.canvas_frame.pack(side=tk.LEFT, anchor=tk.NW)
        # Bind user inputs to function
        self.canvas_frame.bind("<Button-1>", self.draw)
        self.canvas_frame.bind("<B1-Motion>", self.draw)

        self.canvas_frame.focus_set()   # Needed to recognize keyboard commands
        self.canvas_frame.bind("<Tab>", self.goto_next_label)
        self.canvas_frame.bind("<Shift-Tab>", self.goto_prev_label)
        self.canvas_frame.bind("<Return>", self.goto_new_label)
        self.canvas_frame.bind("<Control-s>", self.save)
        self.canvas_frame.bind("<Control-z>", self.erase)

        # Attach image
        self.image = ImageTk.PhotoImage(image)
        self.canvas_frame.create_image(0, 0, anchor=tk.NW, image=self.image)
