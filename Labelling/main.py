import tkinter as tk

from Labelling.config.constants import TEST_IMG_DIR_PATH, TEST_LABEL_DIR_PATH

from Labelling.backend.images import ImagePaths

from Labelling.graphics.bottomtoolbar.bottomtoolbar import BottomToolBar
from Labelling.graphics.menubar.menubar import MenuBar
from Labelling.graphics.toolbar.toolbar import ToolBar
from Labelling.graphics.workspace.workspace import WorkSpace

from Labelling.graphics.file.image_paths import tk_open_dir, tk_open_files


class App:
    def __init__(self):
        # Graphics
        self.root = tk.Tk()
        self.root.title("Computer Vision Labeller")
        self.root.geometry("500x500")   # Makes window size 500x500
        self.menu_bar = MenuBar(self)
        self.tool_bar = ToolBar(self)
        self.workspace = WorkSpace(self)
        self.bottom_tool_bar = BottomToolBar(self)

        # Backend
        self.image_paths: ImagePaths = ImagePaths()

    def add_img_dir(self):
        self.image_paths.load_dir(tk_open_dir())
        self.workspace.display_image(next(self.image_paths))

    def add_img_files(self):
        self.image_paths.load_files(tk_open_files())
        self.workspace.display_image(next(self.image_paths))

    def next_image(self, event=None):
        self.workspace.save()   # Automatically save workspace -- may be unintuitive
        self.workspace.reset_workspace()
        self.workspace.print()
        self.workspace.display_image(app.image_paths.next_image())

    def prev_image(self, event=None):
        self.workspace.save()   # Automatically save workspace -- may be unintuitive
        self.workspace.reset_workspace()
        self.workspace.display_image(app.image_paths.prev_image())
        self.workspace.print()


if __name__ == '__main__':
    app = App()
    app.image_paths.load_dir(TEST_IMG_DIR_PATH)
    app.workspace.display_image(app.image_paths.get_image())
    app.root.mainloop()
