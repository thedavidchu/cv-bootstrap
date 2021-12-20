import tkinter as tk

from Labelling.graphics.common import unimplemented_fnc
from Labelling.graphics.workspace.label import DrawMode


def config_top_menu_bar(app):
    top_menu_bar = tk.Menu(app.root)
    app.root.config(menu=top_menu_bar)

    # File menu
    file_menu = tk.Menu(top_menu_bar, tearoff=0)
    file_menu.add_command(label='New', command=unimplemented_fnc)
    file_menu.add_command(label='Open image directory', command=app.add_img_dir)
    file_menu.add_command(label='Open image file', command=app.add_img_files)
    file_menu.add_command(label='Open label directory', command=unimplemented_fnc)
    file_menu.add_command(label='Open label file', command=unimplemented_fnc)
    file_menu.add_separator()
    file_menu.add_command(label='Save Labels', command=unimplemented_fnc)
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=unimplemented_fnc)
    top_menu_bar.add_cascade(label='File', menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(top_menu_bar, tearoff=0)
    edit_menu.add_command(label='Cursor', command=unimplemented_fnc)
    edit_menu.add_command(label='Add point', command=unimplemented_fnc)
    edit_menu.add_command(label='Add line', command=unimplemented_fnc)
    edit_menu.add_command(label='Add polygon', command=unimplemented_fnc)
    edit_menu.add_command(label='Add custom', command=unimplemented_fnc)
    edit_menu.add_command(label='Add full', command=unimplemented_fnc)
    edit_menu.add_command(label='Add tag', command=unimplemented_fnc)
    top_menu_bar.add_cascade(label='Edit', menu=edit_menu)

    # View menu
    view_menu = tk.Menu(top_menu_bar, tearoff=0)
    view_menu.add_command(label='Zoom in', command=unimplemented_fnc)
    view_menu.add_command(label='Zoom out', command=unimplemented_fnc)
    view_menu.add_command(label='A', command=unimplemented_fnc)
    view_menu.add_command(label='B', command=unimplemented_fnc)
    view_menu.add_command(label='C', command=unimplemented_fnc)
    top_menu_bar.add_cascade(label='View', menu=view_menu)

    # Option menu
    def set_mode_to_none(): app.workspace.labels.get().mode = DrawMode.NONE

    def set_mode_to_point(): app.workspace.labels.get().mode = DrawMode.POINT

    def set_mode_to_line(): app.workspace.labels.get().mode = DrawMode.LINE

    def set_mode_to_polygon(): app.workspace.labels.get().mode = DrawMode.POLYGON

    def set_mode_to_square(): app.workspace.labels.get().mode = DrawMode.SQUARE

    option_menu = tk.Menu(top_menu_bar, tearoff=0)
    option_menu.add_command(label="Mode -> Select", command=set_mode_to_none)
    option_menu.add_command(label="Mode -> Point", command=set_mode_to_point)
    option_menu.add_command(label="Mode -> Line", command=set_mode_to_line)
    option_menu.add_command(label="Mode -> Polygon", command=set_mode_to_polygon)
    option_menu.add_command(label="Mode -> Square", command=set_mode_to_square)
    top_menu_bar.add_cascade(label='Option', menu=option_menu)

    # Help menu
    help_menu = tk.Menu(top_menu_bar, tearoff=0)
    help_menu.add_command(label='Help...', command=unimplemented_fnc)
    top_menu_bar.add_cascade(label='Help', menu=help_menu)


class MenuBar:
    def __init__(self, app):
        self.app = app

        config_top_menu_bar(app)
