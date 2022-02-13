import os
import shutil
import tkinter as tk

from Labelling.constants.constants import LABEL_FILE_EXTENSIONS
from Labelling.backend.move_files import move_files
from Labelling.backend.tk_open_path import tk_open_dir
from Labelling.graphics.popup.popup import show_info


def show_help():
    with open("INSTRUCTIONS.md") as f:
        text = f.read()
    show_info("Instructions", text)
    print(text)


class MenuBar:
    def __init__(self, app):
        self.app = app

        self.config_top_menu_bar()

    def config_top_menu_bar(self):
        app = self.app
        top_menu_bar = tk.Menu(app.root)
        app.root.config(menu=top_menu_bar)

        # File menu
        file_menu = tk.Menu(top_menu_bar, tearoff=0)
        file_menu.add_command(label='Open directory', command=app.add_img_dir)
        file_menu.add_command(label='Open file', command=app.add_img_files)
        file_menu.add_separator()
        file_menu.add_command(label='Export labels', command=self.export_labels)
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

    def export_labels(self, event=None):
        src_dir = tk_open_dir(title="Source directory (where labels are currently)")
        dst_dir = tk_open_dir(title="Destination directory (where to put the labels)")
        return move_files(src_dir, dst_dir, file_ext=LABEL_FILE_EXTENSIONS)
