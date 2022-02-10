import tkinter as tk

from Labelling.graphics.common import build_warning
from Labelling.graphics.workspace.label import DrawMode


class BottomToolBar:
    def __init__(self, app):
        self.app = app

        # Create Frame
        self.bottomtoolbar_frame = tk.LabelFrame(app.root, text="Bottom Tool Bar")
        self.bottomtoolbar_frame.pack(anchor=tk.N, fill="both")

        # Create progress bar
        tk.Label(self.bottomtoolbar_frame, text="Progress").grid(row=0, column=1)
        self.progress_bar = tk.Scale(
            self.bottomtoolbar_frame,
            from_=0,
            to=0,
            orient=tk.HORIZONTAL,
            length=100,
            command=lambda x: self.app.change_image(self.progress_bar.get())
        )
        self.progress_bar.grid(row=0, column=2)

        # Create modes
        tk.Label(self.bottomtoolbar_frame, text="Mode").grid(row=1, column=1)
        self.mode = tk.StringVar(self.bottomtoolbar_frame, DrawMode.POLYGON)
        modes = {
            "Cursor": (DrawMode.NONE, lambda: self.app.workspace.set_mode(DrawMode.NONE)),
            "Point": (DrawMode.POINT, lambda: self.app.workspace.set_mode(DrawMode.POINT)),
            "Line": (DrawMode.LINE, lambda: self.app.workspace.set_mode(DrawMode.LINE)),
            "Polygon": (DrawMode.POLYGON, lambda: self.app.workspace.set_mode(DrawMode.POLYGON)),
        }
        self.radiobutton = []
        for i, (text, (value, cmd)) in enumerate(modes.items()):
            rb = tk.Radiobutton(
                self.bottomtoolbar_frame, text=text, variable=self.mode,
                value=value, indicator=0, background="light blue", command=cmd
            )
            rb.grid(row=1, column=i + 2)
            self.radiobutton.append(rb)
        self.radiobutton[2].select()
        self.mode.set(DrawMode.POLYGON)   # This should set it...

        # Line + Point Colour + Size
        tk.Label(self.bottomtoolbar_frame, text="Line Thickness").grid(row=2, column=1)
        self.line_width = tk.Scale(
            self.bottomtoolbar_frame, from_=0, to=30, orient=tk.HORIZONTAL, length=30,
            command=lambda x: app.workspace.replace_marks(line_colour=app.workspace.focus_colour)
        )
        self.line_width.grid(row=2, column=1)

    def renew_progress_bar(self):
        self.progress_bar.destroy()
        self.progress_bar = tk.Scale(
            self.bottomtoolbar_frame,
            from_=0,
            to=len(self.app.backend.image_paths) - 1,
            orient=tk.HORIZONTAL,
            length=100,
            command=lambda x: self.app.change_image(idx=self.progress_bar.get())
        )
        self.progress_bar.grid(row=0, column=2)