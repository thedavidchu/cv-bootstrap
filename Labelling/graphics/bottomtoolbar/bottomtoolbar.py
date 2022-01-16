import tkinter as tk

from Labelling.graphics.common import build_warning
from Labelling.graphics.workspace.label import DrawMode

def config_tool_bar(app):
    bottomtoolbar_frame = tk.LabelFrame(app.root, text="Blah")
    bottomtoolbar_frame.pack(anchor=tk.N, fill="both")
    misc = []

    # Modes
    tmp = tk.Label(bottomtoolbar_frame, text="Mode").grid(row=0, column=1)
    misc.append(tmp)

    mode = tk.StringVar(bottomtoolbar_frame, "2")
    def set_mode_to_none(): app.workspace.change_mode(DrawMode.NONE)

    def set_mode_to_point(): app.workspace.change_mode(DrawMode.POINT)

    def set_mode_to_line(): app.workspace.change_mode(DrawMode.LINE)

    def set_mode_to_polygon(): app.workspace.change_mode(DrawMode.POLYGON)

    def set_mode_to_square(): app.workspace.change_mode(DrawMode.SQUARE)

    modes = {
        "Cursor": ("0", set_mode_to_none),
        "Point": ("1", set_mode_to_point),
        "Line": ("2", set_mode_to_line),
        "Polygon": ("3", set_mode_to_polygon),
        "Square": ("4", set_mode_to_square)
    }
    for i, (text, (value, cmd)) in enumerate(modes.items()):
        tk.Radiobutton(
            bottomtoolbar_frame, text=text, variable=mode, value=value,
            indicator=0, background="light blue", command=cmd
        ).grid(row=0, column=i+2)

    # Line + Point Colour + Size
    a = tk.Label(bottomtoolbar_frame, text="Line Thickness")
    a.grid(row=1, column=1)
    misc.append(a)

    line_thickness = tk.Scale(
        bottomtoolbar_frame, from_=0, to=20, orient=tk.HORIZONTAL,
        command=lambda x: app.workspace.replace_marks("blue")
    )
    line_thickness.grid(row=2, column=1)

    return bottomtoolbar_frame, line_thickness, misc


class BottomToolBar:
    def __init__(self, app):
        self.app = app
        self.bottomtoolbar_frame, self.line_width, self.misc = config_tool_bar(app)
