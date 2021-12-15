import tkinter as tk

from Labelling.config.constants import TEST_IMG_DIR_PATH, TEST_LABEL_DIR_PATH

from Labelling.backend.images import ImagePaths

from Labelling.graphics.setup import config_geometry

from Labelling.graphics.menubar.menubar import MenuBar
from Labelling.graphics.toolbar.toolbar import ToolBar
from Labelling.graphics.workspace.workspace import WorkSpace

from Labelling.graphics.file.image_paths import tk_open_dir, tk_open_files


class App:
    def __init__(self):
        # Graphics
        self.root = tk.Tk()
        config_geometry(self)
        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.workspace = WorkSpace(self)

        # Backend
        self.image_paths = ImagePaths()

    def __repr__(self):
        return "Computer Vision Labeller"

    def add_img_dir(self):
        self.image_paths.load_dir(tk_open_dir())
        self.workspace.display_image(next(self.image_paths))

    def add_img_files(self):
        self.image_paths.load_files(tk_open_files())
        self.workspace.display_image(next(self.image_paths))


if __name__ == '__main__':
    app = App()
    # config_geometry(app)
    # app.image_paths.load_dir(TEST_IMG_DIR_PATH)
    # app.workspace.display_image(next(app.image_paths))
    app.root.mainloop()
