import os.path
import tkinter as tk
import json
import time
from typing import List, Tuple
from PIL import Image, ImageTk

import warnings

import shapely.geometry as g

from Labelling.common.circular_buffer import CircularBuffer
from Labelling.graphics.workspace.label import DrawMode, Label
from Labelling.graphics.popup.popup import show_prompt, show_warning, show_error


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

        self.mode: DrawMode = DrawMode.POLYGON     # Store previous mode # DEPRECATED
        self.labels: CircularBuffer[Label] = CircularBuffer(Label)
        self.labels.add_item(Label())
        self.labels.get().mode = self.get_mode()  # Initialize mode (default to NONE in deployment)

        self.focus_colour: str = "#ff0000"
        self.background_colour: str = "#00ff00"
        self.line_width: int = 0    # DEPRECATED
        self.image = None
        self.image_size = None # Height, width

    def print(self):
        print(f"Mode: {self.get_mode()}")
        print(f"Labels: {self.labels}")
        print(f"Background Colour: {self.background_colour}")
        print(f"Focus Colour: {self.focus_colour}")

    ############################################################################

    def reset_workspace(self):
        self.labels: CircularBuffer[Label] = CircularBuffer(Label)
        self.labels.add_item(Label())

        self.labels.get().mode = self.get_mode()  # Initialize mode (default to NONE in deployment)

        # Destroy all sub-widgets
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()

        self.image_frame = tk.LabelFrame(self.workspace_frame)
        self.image_frame.pack(anchor=tk.NW)

        self.canvas_frame = None

        self.tag_frame = tk.LabelFrame(self.workspace_frame)
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)

    def load_labels(self):
        label_path: str = self.app.backend.image_paths.get_label_path()
        try:
            with open(label_path) as f:
                r = json.load(f)
        except FileNotFoundError:
            warnings.warn("File not found")
            return False

        if "labels" not in r:
            return False
        labels = r["labels"]
        if not isinstance(labels, list):
            return False
        for raw_label in labels:
            self.goto_new_label()
            label: Label = self.labels.get()
            assert label.loads(raw_label)
            self.mode = label.mode  # Cannot be NONE
            self.background_colour = label.colour if label.colour else self.background_colour
            self.app.bottom_tool_bar.line_width.set(label.width)    # Set width
            line_width = label.width
            self.replace_marks(line_width=line_width)

        self.goto_next_label()

    ############################################################################

    def get_mode(self) -> DrawMode:
        return self.app.bottom_tool_bar.mode

    def set_mode(self, new_mode: DrawMode):
        """Externally called"""
        self.get_label().set_mode(new_mode)
        if new_mode != DrawMode.NONE:
            self.replace_marks(line_colour=self.focus_colour)    # Redraw line in "focus" colour

    def get_colour(self) -> str:
        """Get colour from bottom tool bar."""
        raise NotImplemented

    def set_colour(self, new_colour: str):
        """Externally called"""
        self.get_label().set_colour(new_colour)
        self.replace_marks(line_colour=new_colour)

    def get_line_width(self) -> int:
        return self.app.bottom_tool_bar.line_width

    def set_line_width(self, new_width: int):
        self.line_width = new_width
        self.get_label().set_width(new_width)
        self.replace_marks(
            line_colour=self.focus_colour,
            line_width=self.line_width
        )

    ############################################################################

    # TODO do this
    def get_label(self) -> Label:
        """Get a *reference* to the object holding the points for the current,
        in-focus label"""
        return self.labels.get()

    ############################################################################
    # ==================== MARKS AND POINTS ==================== #
    def record_point(self, x: int, y: int):
        label: Label = self.get_label()
        label.points.append((x, y))

    def draw_point(self, x: int, y: int, colour: str, width: int):
        r = max(1, width // 2)
        point_mark = self.canvas_frame.create_oval(
            x - r, y - r, x + r, y + r, fill=colour,
            outline="")
        self.get_label().marks.append(point_mark)

    def draw_line(self, x: int, y:int, colour: str, width: int):
        """Assumes that there is a previous point!"""
        label: Label = self.get_label()

        # Draw line
        prev_x, prev_y = label.points[-1] if label.points else (None, None)
        if prev_x is None or prev_y is None:
            raise ValueError("expected previous point to exist")
        line_mark = self.canvas_frame.create_line(
            x,
            y,
            prev_x,
            prev_y,
            fill=colour,
            width=width,
        )
        self.get_label().marks.append(line_mark)

    def handle_click(self, event):
        x, y = event.x, event.y

        mode: DrawMode = self.get_mode()

        if mode == DrawMode.NONE:
            # Do nothing (don't even add point)
            pass
        elif mode == DrawMode.POINT:
            # Convert points to individual points
            self.record_point(x=x, y=y)
            self.draw_point(x=x, y=y, colour=self.focus_colour, width=self.line_width)
        elif mode == DrawMode.LINE:
            if self.get_label().points:  # We have at least one previous point
                self.draw_line(x=x, y=y, colour=self.focus_colour, width=self.line_width)
            self.record_point(x=x, y=y)     # This is after the previous in case we get an error
            self.draw_point(x=x, y=y, colour=self.focus_colour, width=self.line_width)
        elif mode == DrawMode.POLYGON:
            if self.get_label().points:  # We have at least one previous point
                self.draw_line(x=x, y=y, colour=self.focus_colour, width=self.line_width)
            self.record_point(x=x, y=y)     # This is after the previous in case we get an error
            self.draw_point(x=x, y=y, colour=self.focus_colour, width=self.line_width)
        elif mode == DrawMode.SQUARE:
            show_warning("Square Mode is Not Implemented")
        else:
            show_error("This mode is Not Implemented yet. In fact, I did not even know it existed!")

    ############################################################################

    def delete_one_point(self):
        points: List[Tuple[int, int]] = self.get_label().points
        if points:
            points.pop(-1)

    def delete_all_points(self):
        """Delete all points in the current focussed geometry."""
        self.get_label().points = []

    def erase_one_mark(self):
        current_label: Label = self.get_label()
        num_points = len(current_label.points)
        num_marks = len(current_label.marks)
        if num_points == 0:
            # Nothing to delete
            assert num_marks == 0
        elif num_points == 1:
            # If there is a single point, there shall be no connecting line to
            # any other point.
            assert num_marks == 1
            self.canvas_frame.delete(current_label.marks.pop(-1))
        # Should this get the mode from the label or from the bottom tool bar?
        elif current_label.mode == DrawMode.POINT:
            # There should be the same number of points as marks
            assert num_points == num_marks
            self.canvas_frame.delete(current_label.marks.pop(-1))
        else:
            # If there are N points (where N > 1), then there should be either
            # `2 * N - 1` if it is not closed or `2 * N` if it is closed
            assert num_marks == 2 * num_points - 1 or num_marks == 2 * num_points
            self.canvas_frame.delete(current_label.marks.pop(-1))
            self.canvas_frame.delete(current_label.marks.pop(-1))

    def erase_all_marks(self):
        """Delete all marks in the current focussed geometry."""
        current_label: Label = self.get_label()
        current_label.points = []
        # TODO: test `map(self.canvas_frame.delete, current_label.marks)`
        for mark in current_label.marks:
            self.canvas_frame.delete(mark)

    def handle_backspace(self):
        self.delete_one_point()
        self.erase_one_mark()

    def handle_delete(self):
        self.delete_all_points()
        self.erase_all_marks()

    ############################################################################

    def replace(self,
        line_colour: str,
        line_width: int,
    ):
        self.erase_all_marks()
        for point in self.get_label().points:
            self.draw(
                g.Point(point),
                line_colour=line_colour,
                line_width=line_width,
            )

    ############################################################################

    def finish_label(self):
        """Finish a label"""
        # Complete polygon, draw partially transparent polygon on canvas

    def save_all_labels(self):
        self.finish_label()

        # Prompt to record author if missing (repeatedly if necessary)
        while not self.app.backend.author:
            self.app.backend.author = show_prompt(
                "Author missing", "Author must be specified!"
            )

        obj_to_write = {
            "path": self.app.backend.image_paths.get_image_path(),
            "categories": [
                "TODO - the categories of objects (in numerical order)"],
            "category_colours": [
                "TODO - map categories -> (focus, background colours)"],
            "labels": [
                label.dumps() for label in self.labels.to_list() if label
            ],
            "image_size": self.image_size,
            "author": self.app.backend.author,
            "timestamp": time.time(),
        }
        label_path: str = self.app.backend.image_paths.get_label_path()
        # Save only if change is made
        with open(label_path) as f:
            obj_to_read = json.load(f)
        if not all(
            # Check all _except_ timestamp is identical
            obj_to_read[key] == obj_to_write[key]
            for key in obj_to_write.keys() if key != "timestamp"
        ):
            with open(label_path, "w") as f:
                json.dump(obj=obj_to_write, fp=f, indent=4)

    ############################################################################

    ### WARNING ALL BELOW ARE DEPRECATED ###

    def draw(self, event=None, *, line_colour=None, line_width=None):
        """Draw points on the screen and write points to labels."""
        # Parse arguments
        x, y = event.x, event.y
        line_colour = self.focus_colour if line_colour is None else line_colour
        line_width = self.app.bottom_tool_bar.line_width.get() if line_width is None else line_width

        # Get current status
        current_label: Label = self.labels.get()
        current_label.width = line_width
        self.mode = current_label.mode  # Set mode to current label's mode
        points = current_label.points
        prev_x, prev_y = points[-1] if points else (None, None)
        points.append((x, y))   # Add point to label's list of points (spooky action at a distance)
        mode = current_label.mode   # TODO - Better in match-case statement
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
                    width=line_width,
                )
                current_label.marks.append(line)
        else:
            raise NotImplementedError("unsupported drawing mode")
        r = max(1, line_width // 2)
        point_mark = self.canvas_frame.create_oval(
            x - r, y - r, x + r, y + r, fill=line_colour,
            outline="")
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

    def erase_current_label(self, event=None):
        """ Erase the entirety of the current label.
        NOTE - this can't currently be undone, which is very scary!"""
        num = len(self.labels.get().points)
        for _ in range(num):
            self.erase()

    def replace_marks(self, *, line_colour=None, line_width=None):
        """ Replace an on-screen annotation with a different colour in the same mode. """
        line_colour = self.background_colour if line_colour is None else line_colour
        line_width = self.app.bottom_tool_bar.line_width.get() if line_width is None else line_width

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
            self.draw(g.Point(*point), line_colour=line_colour, line_width=line_width)

    # ==================== WHICH LABELS ==================== #
    # Just completes polygons, doesn't actually do any writing
    def write_to_label(self):
        """ Writes to label. NOTE - this doesn't actually happen here. It happens in draw. """
        current_label: Label = self.labels.get()
        # Complete Polygon if applicable
        if current_label.mode == DrawMode.POLYGON and len(current_label.points) >= 2:
            x, y = current_label.points[0]
            self.draw(g.Point(x, y))

    ### TODO remake these in a cleaner fashion

    def goto_next_label(self, event=None):
        """ Advance to the next label without saving to file. """
        if len(self.labels) == 1:   # Prevent deleting only one
            return
        elif not self.labels.get():
            self.labels.delete_current()    # Goto next is implicit
        else:
            self.write_to_label()
            self.replace_marks(line_colour=self.background_colour)    # Redraw line in "background" colour
            self.labels.next()
        self.replace_marks(line_colour=self.focus_colour)       # Redraw line in "focus" colour
        self.set_mode(self.labels.get().mode)    # Also redraws line (redundantly)

    def goto_prev_label(self, event=None):
        """ Go to the previous label without saving to file. """
        if len(self.labels) == 1:   # Prevent deleting only one
            return
        elif not self.labels.get():
            self.labels.delete_current()    # Goto prev not implicit
        else:
            self.write_to_label()
            self.replace_marks(line_colour=self.background_colour)    # Redraw line in "background" colour
        self.labels.prev()
        self.replace_marks(line_colour=self.focus_colour)  # Redraw line in "focus" colour
        self.set_mode(self.labels.get().mode)  # Also redraws line (redundantly)

    def goto_new_label(self, event=None):
        """ Go to the next, newly created label unless the current label has no points. """
        if self.labels.get().points:
            draw_mode = self.labels.get().mode
            self.write_to_label()
            self.replace_marks(line_colour=self.background_colour)  # Redraw line in "background" colour
            # Create new label and switch to it
            self.labels.insert_after_current(Label())
            self.labels.next()
            # Set draw mode the same as previously
            self.labels.get().mode = draw_mode
            self.replace_marks(line_colour=self.focus_colour)  # Redraw line in "focus" colour
            self.set_mode(self.labels.get().mode)  # Also redraws line (redundantly)
        else:
            # Empty label, so don't write
            pass

    # ==================== SAVING ==================== #
    def save(self, event=None):
        """ Save all labels. """
        self.write_to_label()

        # Get author
        while not self.app.backend.author:
            self.app.backend.author = show_prompt("Author missing", "Author constant must be specified")

        r = {
            "path": self.app.backend.image_paths.get_image_path(),
            "categories": ["TODO - the categories of objects (in numerical order)"],
            "category_colours": ["TODO - map categories -> (focus, background colours)"],
            "labels": [label.dumps() for label in self.labels if label],
            "image_size": self.image_size,
            "author": self.app.backend.author,
            "timestamp": time.time(),
        }
        label_path: str = self.app.backend.image_paths.get_label_path()
        with open(label_path, "w") as f:
            json.dump(obj=r, fp=f, indent=4)

    def display_image(self, image: Image):
        width, height = image.size
        self.image_size = [height, width]

        self.canvas_frame = tk.Canvas(master=self.image_frame, width=width, height=height)
        self.canvas_frame.pack(side=tk.LEFT, anchor=tk.NW)
        # Bind user inputs to function
        self.canvas_frame.bind("<Button-1>", self.handle_click)
        self.canvas_frame.bind("<B1-Motion>", self.handle_click)

        self.canvas_frame.focus_set()   # Needed to recognize keyboard commands
        self.canvas_frame.bind("<Right>", self.goto_next_label)
        self.canvas_frame.bind("<Left>", self.goto_prev_label)
        self.canvas_frame.bind("<Delete>", self.handle_delete)
        self.canvas_frame.bind("<Return>", self.goto_new_label)
        self.canvas_frame.bind("<Control-s>", self.save)
        self.canvas_frame.bind("<BackSpace>", self.handle_backspace)
        self.canvas_frame.bind("<greater>", self.app.next_image)
        self.canvas_frame.bind("<less>", self.app.prev_image)

        # Attach image
        self.image = ImageTk.PhotoImage(image)
        self.canvas_frame.create_image(0, 0, anchor=tk.NW, image=self.image)

        # Load if applicable
        self.load_labels()