import tkinter as tk

from Labelling.graphics.common import unimplemented_fnc, build_warning
from Labelling.graphics.workspace.label import DrawMode


def config_top_menu_bar(app):
    top_menu_bar = tk.Menu(app.root)
    app.root.config(menu=top_menu_bar)

    # File menu
    file_menu = tk.Menu(top_menu_bar, tearoff=0)
    file_menu.add_command(label='New', command=unimplemented_fnc)
    file_menu.add_command(label='Open image directory', command=app.add_img_dir)
    file_menu.add_command(label='Open image file', command=app.add_img_files)
    file_menu.add_command(label='Open label directory', command=build_warning("File::Cursor"))
    file_menu.add_command(label='Open label file', command=build_warning("File::Open label file"))
    file_menu.add_separator()
    file_menu.add_command(label='Save Labels', command=build_warning("File::Save Labels"))
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=build_warning("Edit::Cursor"))
    top_menu_bar.add_cascade(label='File', menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(top_menu_bar, tearoff=0)
    edit_menu.add_command(label='Cursor', command=build_warning("Edit::Cursor"))
    edit_menu.add_command(label='Add point', command=build_warning("Edit::Add point"))
    edit_menu.add_command(label='Add line', command=build_warning("Edit::Add line"))
    edit_menu.add_command(label='Add polygon', command=build_warning("Edit::Add polygon"))
    edit_menu.add_command(label='Add custom', command=build_warning("Edit::Add custom"))
    edit_menu.add_command(label='Add full', command=build_warning("Edit::Add full"))
    edit_menu.add_command(label='Add tag', command=build_warning("Edit::Add tag"))
    top_menu_bar.add_cascade(label='Edit', menu=edit_menu)

    # View menu
    view_menu = tk.Menu(top_menu_bar, tearoff=0)
    view_menu.add_command(label='Zoom in', command=build_warning("View::Zoom in"))
    view_menu.add_command(label='Zoom out', command=build_warning("View::Zoom out"))
    view_menu.add_command(label='A', command=build_warning("View::A"))
    view_menu.add_command(label='B', command=build_warning("View::B"))
    view_menu.add_command(label='C', command=build_warning("View::C"))
    top_menu_bar.add_cascade(label='View', menu=view_menu)

    # Option menu
    def set_mode_to_none(): app.workspace.change_mode(DrawMode.NONE)

    def set_mode_to_point(): app.workspace.change_mode(DrawMode.POINT)

    def set_mode_to_line(): app.workspace.change_mode(DrawMode.LINE)

    def set_mode_to_polygon(): app.workspace.change_mode(DrawMode.POLYGON)

    def set_mode_to_square(): app.workspace.change_mode(DrawMode.SQUARE)

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
