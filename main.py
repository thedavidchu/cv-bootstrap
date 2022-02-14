import tkinter as tk

from Labelling.backend.images import ImagePaths

from Labelling.backend.backend import Backend
from Labelling.backend.tk_open_path import tk_open_dir, tk_open_files

from Labelling.graphics.bottomtoolbar.bottomtoolbar import BottomToolBar
from Labelling.graphics.menubar.menubar import MenuBar
from Labelling.graphics.toolbar.toolbar import ToolBar
from Labelling.graphics.workspace.workspace import WorkSpace

from Labelling.graphics.popup import popup


class App:
    def __init__(self):
        # Graphics
        self.root = tk.Tk()
        self.root.title("Computer Vision Labeller")
        self.root.geometry("500x500")   # Makes window size 500x500

        # Backend
        self.backend: Backend = Backend(self)

        self.menu_bar: MenuBar = MenuBar(self)
        self.tool_bar: ToolBar = ToolBar(self)
        self.workspace: WorkSpace = WorkSpace(self)
        self.bottom_tool_bar: BottomToolBar = BottomToolBar(self)

    def setup_images(self):
        """Setup the images, labels, and progress bar (refreshed with new number
        of items."""
        self.bottom_tool_bar.renew_progress_bar()
        self.workspace.display_image_and_labels_and_bind_keyboard(
            self.backend.image_paths.get_image(),
            self.backend.image_paths.get_label_path(),
        )

    def add_img_dir(self):
        self.backend.image_paths.load_dir(tk_open_dir())
        self.setup_images()

    def add_img_files(self):
        self.backend.image_paths.load_files(tk_open_files())
        self.setup_images()

    def change_image(self, event=None, idx: int = None):
        self.workspace.set_image(
            old_image_path=self.backend.image_paths.get_image_path(),
            old_label_path=self.backend.image_paths.get_label_path(),
            new_image=self.backend.image_paths.set_image(idx),
            new_label_path=self.backend.image_paths.get_label_path(),
        )
        self.bottom_tool_bar.progress_bar.set(self.backend.image_paths.get_idx())
        print(f"Image: {self.backend.image_paths.get_image_path()}")

    def next_image(self, event=None):
        self.workspace.set_image(
            old_image_path=self.backend.image_paths.get_image_path(),
            old_label_path=self.backend.image_paths.get_label_path(),
            new_image=self.backend.image_paths.next_image(),
            new_label_path=self.backend.image_paths.get_label_path(),
        )
        self.bottom_tool_bar.progress_bar.set(self.backend.image_paths.get_idx())
        print(f"Image: {self.backend.image_paths.get_image_path()}")

    def prev_image(self, event=None):
        self.workspace.set_image(
            old_image_path=self.backend.image_paths.get_image_path(),
            old_label_path=self.backend.image_paths.get_label_path(),
            new_image=self.backend.image_paths.prev_image(),
            new_label_path=self.backend.image_paths.get_label_path(),
        )
        self.bottom_tool_bar.progress_bar.set(self.backend.image_paths.get_idx())
        print(f"Image: {self.backend.image_paths.get_image_path()}")


if __name__ == '__main__':
    app = App()
    app.bottom_tool_bar.line_width.set(1)
    app.root.mainloop()
