import tkinter as tk

from Labelling.graphics.common import build_warning
from Labelling.graphics.workspace.label import DrawMode

def config_tool_bar(app):
    bottomtoolbar_frame = tk.LabelFrame(app.root, text="Bottom Tool Bar")
    bottomtoolbar_frame.pack(anchor=tk.N, fill="both")
    misc = []

    # Modes
    tmp = tk.Label(bottomtoolbar_frame, text="Mode").grid(row=0, column=1)
    misc.append(tmp)
    mode = tk.StringVar(bottomtoolbar_frame, "2")
    modes = {
        "Cursor": ("0", lambda: app.workspace.change_mode(DrawMode.NONE)),
        "Point": ("1", lambda: app.workspace.change_mode(DrawMode.POINT)),
        "Line": ("2", lambda: app.workspace.change_mode(DrawMode.LINE)),
        "Polygon": ("3", lambda: app.workspace.change_mode(DrawMode.POLYGON)),
        "Square": ("4", lambda: app.workspace.change_mode(DrawMode.SQUARE))
    }
    rb = []
    for i, (text, (value, cmd)) in enumerate(modes.items()):
        rb.append(
            tk.Radiobutton(
                bottomtoolbar_frame, text=text, variable=mode, value=value,
                indicator=0, background="light blue", command=cmd
            )
        )
        rb[-1].grid(row=0, column=i+2)
    rb[2].select()
    mode.set("2")

    # Line + Point Colour + Size
    a = tk.Label(bottomtoolbar_frame, text="Line Thickness")
    a.grid(row=1, column=1)
    misc.append(a)

    line_thickness = tk.Scale(
        bottomtoolbar_frame, from_=0, to=20, orient=tk.HORIZONTAL,
        command=lambda x: app.workspace.replace_marks(app.workspace.focus_colour)
    )
    line_thickness.grid(row=2, column=1)

    return bottomtoolbar_frame, line_thickness, misc


class BottomToolBar:
    def __init__(self, app):
        self.app = app
        self.bottomtoolbar_frame, self.line_width, self.misc = config_tool_bar(app)
