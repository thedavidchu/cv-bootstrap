import tkinter as tk

from Labelling.graphics.popup.popup import show_info


def show_help():
    with open("INSTRUCTIONS.md") as f:
        text = f.read()
    show_info("Instructions", text)
    print(text)


def config_top_menu_bar(app):
    top_menu_bar = tk.Menu(app.root)
    app.root.config(menu=top_menu_bar)

    # File menu
    file_menu = tk.Menu(top_menu_bar, tearoff=0)
    file_menu.add_command(label='Open directory', command=app.add_img_dir)
    file_menu.add_command(label='Open file', command=app.add_img_files)
    top_menu_bar.add_cascade(label='File', menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(top_menu_bar, tearoff=0)
    top_menu_bar.add_cascade(label='Edit', menu=edit_menu)

    # View menu
    view_menu = tk.Menu(top_menu_bar, tearoff=0)
    top_menu_bar.add_cascade(label='View', menu=view_menu)

    # Help menu
    help_menu = tk.Menu(top_menu_bar, tearoff=0)
    help_menu.add_command(label='Help...', command=show_help)
    top_menu_bar.add_cascade(label='Help', menu=help_menu)


class MenuBar:
    def __init__(self, app):
        self.app = app

        config_top_menu_bar(app)
