import tkinter as tk

from Labelling.config.constants import TEST_IMG_DIR_PATH, TEST_LABEL_DIR_PATH

from Labelling.backend.images import ImagePaths

from Labelling.graphics.setup import config_geometry, config_top_menu_bar
from Labelling.graphics.file.image_paths import tk_open_dir, tk_open_files
from Labelling.graphics.image.display import Display


class App():
    def __init__(self):
        self.root = tk.Tk()
        self.image_paths = ImagePaths()
        self.display = Display(self.root)

    def __repr__(self):
        return "Computer Vision Labeller"

    def add_img_dir(self):
        self.image_paths.load_dir(tk_open_dir())
        self.display.display_next_image(next(self.image_paths))

    def add_img_files(self):
        self.image_paths.load_files(tk_open_files())
        self.display.display_next_image(next(self.image_paths))


if __name__ == '__main__':
    app = App()
    config_geometry(app)
    config_top_menu_bar(app)
    app.image_paths.load_dir(TEST_IMG_DIR_PATH)
    app.display.display_next_image(next(app.image_paths))
    app.root.mainloop()
