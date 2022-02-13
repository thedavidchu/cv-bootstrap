import os.path
import tkinter as tk
import json
import time
from typing import List, Tuple
from PIL import Image, ImageTk

import warnings

import shapely.geometry as g

from Labelling.backend.label import DrawMode, Label
from Labelling.common.circular_buffer import CircularBuffer
from Labelling.graphics.popup.popup import show_prompt, show_warning, show_error


class WorkSpace:
    def __init__(self, app):
        self.app = app
        # Main workspace frame
        self.workspace_frame = tk.LabelFrame(app.root)
        self.workspace_frame.pack(anchor=tk.N, fill="both")
        # Image frame for holding the image we will label
        self.image_frame = tk.LabelFrame(self.workspace_frame)
        self.image_frame.pack(anchor=tk.NW)
        # We create the canvas frame each time we get a new image
        self.canvas_frame = None
        # Tag frame for holding information about the category of the labels
        self.tag_frame = tk.LabelFrame(self.workspace_frame)
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)
        # Labels
        self.labels: CircularBuffer[Label] = CircularBuffer(Label)
        self.labels.insert(Label())
        # Set the mode to the mode on the buttons
        self.get_label().mode = DrawMode.POLYGON
        # These colours will be deprecated once you can select the colour in the
        # bottom tool bar
        self.focus_colour: str = "#ff0000"  # Red
        self.background_colour: str = "#00ff00"  # Green
        self.image = None
        self.image_size = None  # Height, width

    ############################################################################

    ####
    #   CONVENIENCE FUNCTIONS
    ####

    def get_label(self) -> Label:
        """Get a *reference* to the object holding the points for the current,
        in-focus label"""
        return self.labels.get()

    def print(self):
        print(f"Mode: {self.get_mode()}")
        print(f"Labels: {self.labels}")
        print(f"Background Colour: {self.background_colour}")
        print(f"Focus Colour: {self.focus_colour}")

    ############################################################################

    def reset_workspace(self):
        """Reset the workspace to the blank slate."""
        self.labels: CircularBuffer[Label] = CircularBuffer(Label)
        self.labels.insert(Label())

        self.set_mode(self.get_mode())

        # Destroy all drawings
        for widget in self.workspace_frame.winfo_children():
            widget.destroy()

        # Delete image, canvas, and tag frames
        self.image_frame = tk.LabelFrame(self.workspace_frame)
        self.image_frame.pack(anchor=tk.NW)
        self.canvas_frame = None
        self.tag_frame = tk.LabelFrame(self.workspace_frame)
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)

    def load_labels(self):
        label_path: str = self.app.backend.image_paths.get_label_path()
        # Try to load the json file
        try:
            with open(label_path) as f:
                obj = json.load(f)
        except FileNotFoundError:
            # Not a big deal, it just means we haven't started labelling this
            # image.
            warnings.warn("File not found")
            return False

        if "labels" not in obj:
            return False
        labels = obj["labels"]
        if not isinstance(labels, list):
            return False
        for raw_label in labels:
            self.goto_new_label()
            label: Label = self.labels.get()
            assert label.loads(raw_label)
            self.mode = label.mode  # Cannot be NONE
            self.background_colour = label.colour if label.colour else self.background_colour
            self.app.bottom_tool_bar.line_width.set(label.width)    # Set width
            self.replace_focused(
                line_colour=self.focus_colour, line_width=label.width
            )

        self.goto_next_label()

    ############################################################################

    def get_mode(self) -> DrawMode:
        return self.app.bottom_tool_bar.mode.get()

    def set_mode(self, new_mode: DrawMode):
        """Change the mode and redraw the line."""
        self.get_label().set_mode(new_mode)
        # Set the button to the set mode (NOTE: we cannot call a function,
        # because that function may call this one, which would lead to infinite
        # recursion.
        self.app.bottom_tool_bar.mode.set(new_mode)
        if new_mode != DrawMode.NONE:
            # Redraw line in "focus" colour
            self.replace_focused(
                line_colour=self.focus_colour, line_width=self.get_line_width()
            )

    def get_colour(self) -> str:
        """Get colour from bottom tool bar."""
        raise NotImplemented

    def set_colour(self, new_colour: str):
        """Externally called"""
        self.get_label().set_colour(new_colour)
        self.replace_focused(
            line_colour=new_colour, line_width=self.get_line_width()
        )

    def get_line_width(self) -> int:
        return self.app.bottom_tool_bar.line_width.get()

    def set_line_width(self, new_width: int):
        self.get_label().set_width(new_width)
        # We cannot call the below in a function from bottom_tool_bar in case
        # that function calls this one. That would lead to catastrophic infinite
        # recursion.
        self.app.bottom_tool_bar.line_width.set(new_width)
        self.replace_focused(
            line_colour=self.focus_colour, line_width=new_width
        )

    ############################################################################

    def record_point(self, x: int, y: int):
        label: Label = self.get_label()
        label.points.append((x, y))

    def draw_point(self, x: int, y: int, colour: str, width: int):
        r = max(1, width // 2)
        point_mark = self.canvas_frame.create_oval(
            x - r, y - r, x + r, y + r, fill=colour,
            outline="")
        self.get_label().marks.append(point_mark)

    def draw_line(
        self, x0: int, y0: int, x1: int, y1: int, colour: str, width: int
    ):
        """Draw a point between two points."""
        label: Label = self.get_label()

        # Draw line
        line_mark = self.canvas_frame.create_line(
            x0,
            y0,
            x1,
            y1,
            fill=colour,
            width=width,
        )
        self.get_label().marks.append(line_mark)

    def draw(
        self,
        mode: DrawMode,
        x: int, y: int,
        prev_x: int, prev_y: int,
        colour: str, width: int,
        record_point: bool,
    ):
        if mode == DrawMode.NONE:
            # Do nothing (don't even add point)
            pass
        elif mode == DrawMode.POINT:
            # Convert points to individual points
            if record_point:
                self.record_point(x=x, y=y)
            self.draw_point(x=x, y=y, colour=colour, width=width)
        elif mode == DrawMode.LINE:
            # We have at least one previous point
            if prev_x is not None and prev_y is not None:
                self.draw_line(
                    x0=x, y0=y, x1=prev_x, y1=prev_y, colour=colour,
                    width=width
                )
            # This is after the previous in case we get an error
            if record_point:
                self.record_point(x=x, y=y)
            self.draw_point(x=x, y=y, colour=colour, width=width)
        elif mode == DrawMode.POLYGON:
            # We have at least one previous point
            if prev_x is not None and prev_y is not None:
                self.draw_line(
                    x0=x, y0=y, x1=prev_x, y1=prev_y, colour=colour,
                    width=width
                )
            # This is after the previous in case we get an error
            if record_point:
                self.record_point(x=x, y=y)
            self.draw_point(x=x, y=y, colour=colour, width=width)
        elif mode == DrawMode.SQUARE:
            show_warning("Square Mode is Not Implemented")
        else:
            show_error(
                f"This mode ({mode}) is Not Implemented yet. "
                f"In fact, I did not even know it existed!"
            )

    def handle_click(self, event):
        prev_point = (
            self.get_label().points[-1]
            if self.get_label().points
            else (None, None)
        )
        self.draw(
            mode=self.get_mode(),
            x=event.x, y=event.y,
            prev_x=prev_point[0], prev_y=prev_point[1],
            colour=self.focus_colour, width=self.get_line_width(),
            record_point=True
        )

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

    def erase_focused(self):
        """Delete all marks in the current focussed geometry."""
        current_label: Label = self.get_label()
        # TODO: test `map(self.canvas_frame.delete, current_label.marks)`
        # map(self.canvas_frame.delete, current_label.marks)
        for mark in current_label.marks:
            self.canvas_frame.delete(mark)

    def handle_backspace(self, _=None):
        self.delete_one_point()
        self.erase_one_mark()

    def handle_delete(self, _=None):
        self.delete_all_points()
        self.erase_focused()

    ############################################################################

    def replace_focused(
        self, line_colour: str, line_width: int,
    ):
        """Draw or redraw the focussed line."""
        self.erase_focused()
        mode = self.get_mode()
        prev_x, prev_y = None, None
        for x, y in self.get_label().points:
            self.draw(
                mode=mode,
                x=x, y=y,
                prev_x=prev_x, prev_y=prev_y,
                colour=line_colour, width=line_width,
                # Do not record point, otherwise this will lead to an infinite
                # loop as we add to the list we are iterating over
                record_point=False,
            )
            # Remember previous x, y
            prev_x, prev_y = x, y

    ############################################################################

    def finish_label(self):
        """Finish a label"""
        # Complete polygon, draw partially transparent polygon on canvas
        if self.get_mode() == DrawMode.POLYGON and len(self.get_label().points) > 1:
            first_x, first_y = self.get_label().points[0]
            last_x, last_y = self.get_label().points[-1]
            # Already connected
            if first_x == last_x and first_y == last_y:
                pass
            # Draw completion
            else:
                self.handle_click(g.Point(first_x, first_y))

    def save_all_labels(self, _=None):
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

    ####
    #   LABELS IN SAME IMAGE
    ####

    def goto_next_label(self, _=None):
        """Advance to the next label without saving to file."""
        # If there is only one image, then stay on current image
        if len(self.labels) == 1:
            # Having this as a separate case ensures that this does not get
            # deleted if the current label is an empty pattern. It also avoids
            # having to redraw the line.
            return
        elif not self.labels.get():
            # Go to next is implicit
            self.labels.delete()
        else:
            self.finish_label()
            # Redraw current line in "background" colour
            self.replace_focused(
                line_colour=self.background_colour,
                line_width=self.get_line_width(),
            )
            self.labels.next()
        # Set the mode as the stored mode for the next label and redraw line in
        # the "focus" colour
        self.set_mode(self.labels.get().mode)

    def goto_prev_label(self, _=None):
        """Go to the previous label without saving to file."""
        # If there is only one image, then stay on current image
        if len(self.labels) == 1:
            # Having this as a separate case ensures that this does not get
            # deleted if the current label is an empty pattern. It also avoids
            # having to redraw the line.
            return
        elif not self.labels.get():
            # Go to previous is NOT implicit
            self.labels.delete()
        else:
            self.finish_label()
            # Redraw current line in "background" colour
            self.replace_focused(
                line_colour=self.background_colour,
                line_width=self.get_line_width(),
            )
        self.labels.prev()
        # Set the mode as the stored mode for the next label and redraw line in
        # the "focus" colour
        self.set_mode(self.labels.get().mode)

    def goto_new_label(self, _=None):
        """Go to the next, newly created label unless the current label has no
        points."""
        if not self.labels.get().points:
            # Empty label, so stay on the current label
            return
        # Record the mode for the current line
        draw_mode = self.labels.get().mode
        # Save and redraw the line in the "background" colour
        self.finish_label()
        self.replace_focused(
            line_colour=self.background_colour, line_width=self.get_line_width()
        )
        # Create new label and switch to it implicitly
        self.labels.insert(Label())
        # Set draw mode the same as previously and set the mode as the stored
        # mode for the next label and redraw line in the "focus" colour
        self.labels.get().mode = draw_mode
        self.set_mode(draw_mode)

    ############################################################################

    def display_image(self, image: Image):
        width, height = image.size
        self.image_size = [height, width]
        self.canvas_frame = tk.Canvas(
            master=self.image_frame, width=width, height=height
        )
        self.canvas_frame.pack(side=tk.LEFT, anchor=tk.NW)
        # Bind user inputs to function
        self.canvas_frame.bind("<Button-1>", self.handle_click)
        self.canvas_frame.bind("<B1-Motion>", self.handle_click)
        # Keyboard commands
        self.canvas_frame.focus_set()   # Needed to recognize keyboard commands
        self.canvas_frame.bind("<Right>", self.goto_next_label)
        self.canvas_frame.bind("<Left>", self.goto_prev_label)
        self.canvas_frame.bind("<Delete>", self.handle_delete)
        self.canvas_frame.bind("<Return>", self.goto_new_label)
        self.canvas_frame.bind("<Control-s>", self.save_all_labels)
        self.canvas_frame.bind("<BackSpace>", self.handle_backspace)
        # External commands
        self.canvas_frame.bind("<greater>", self.app.next_image)
        self.canvas_frame.bind("<less>", self.app.prev_image)
        # Attach image
        self.image = ImageTk.PhotoImage(image)
        self.canvas_frame.create_image(0, 0, anchor=tk.NW, image=self.image)
        # Load if applicable
        self.load_labels()