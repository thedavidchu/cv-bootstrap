import tkinter as tk

from setup import config_top_menu_bar


if __name__ == "__main__":
    DEFAULT_IMAGE_PATH = "C:/Users/theda/PycharmProjects/cv-bootstrap/data/images"
    DEFAULT_LABEL_PATH = "C:/Users/theda/PycharmProjects/cv-bootstrap/data/labels"

    root = tk.Tk()
    config_top_menu_bar(root)
    root.mainloop()
