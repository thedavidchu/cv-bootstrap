import tkinter as tk
import tkinter.filedialog  # Necessary
from typing import Tuple

from Labelling.config.constants import TEST_IMG_DIR_PATH


def tk_open_dir() -> str:
    dir_path = tk.filedialog.askdirectory(initialdir=TEST_IMG_DIR_PATH)
    return dir_path


def tk_open_files() -> Tuple[str]:
    file_paths = tk.filedialog.askopenfilenames(initialdir=TEST_IMG_DIR_PATH)
    return file_paths


if __name__ == '__main__':
    root = tk.Tk()
    dir_path = tk_open_dir()
    file_paths = tk_open_files()
    tk.mainloop()
