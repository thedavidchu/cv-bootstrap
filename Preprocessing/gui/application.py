import tkinter as tk
import tkinter.filedialog  # Necessary
from PIL import Image, ImageTk
from Preprocessing.server.path import get_image_paths, filter_image_paths
import warnings


class Display:
    def __init__(self, root):
        self.root = root

        self.menubar = None
        self.buttons = {}

        # image_index = -1 => start at beginning
        self.image_paths = []
        self.image_index = -1

        self.image = None
        self.panel = None

    def __no_images(self):
        return len(self.image_paths) == 0

    def __calculate_next_image_index(self, offset: int = 1):
        self.image_index = (self.image_index + offset) % len(self.image_paths)

    def display_workspace(self):
        sassy_warning = lambda: warnings.warn('lol this does not do anything!')

        # Do on __init__?
        self.root.geometry('500x500')

        # Add menu
        self.menubar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label='New', command=sassy_warning)
        file_menu.add_command(label='Open directory', command=self.open_dir)
        file_menu.add_command(label='Open file', command=self.open_file)
        file_menu.add_command(label='Save (ENTER)', command=sassy_warning)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.destroy)
        self.menubar.add_cascade(label='File', menu=file_menu)

        edit_menu = tk.Menu(self.menubar, tearoff=0)
        edit_menu.add_command(label='Cursor')
        edit_menu.add_command(label='Add point')
        edit_menu.add_command(label='Add line')
        edit_menu.add_command(label='Add polygon')
        edit_menu.add_command(label='Add point')
        edit_menu.add_command(label='Add point')

        self.menubar.add_cascade(label='Edit', menu=edit_menu)

        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label='Help...', command=sassy_warning)

        root.config(menu=self.menubar)


    def open_dir(self):
        # Hide workspace window
        self.root.withdraw()
        # Open '//images' directory by default
        dir_path = tk.filedialog.askdirectory(initialdir='../../')
        try:
            self.image_paths = get_image_paths(dir_path)
        except:
            warnings.warn('invalid directory chosen')
        # Reset image index
        self.image_index = -1
        # Show workspace window
        self.root.deiconify()
        # Show first image
        self.display_next_image()

    def open_file(self):
        # Hide workspace window
        self.root.withdraw()
        # Open '//images' directory by default
        image_paths = tk.filedialog.askopenfilenames(initialdir='../../')
        self.image_paths = filter_image_paths(image_paths)
        print(self.image_paths)
        # Reset image index
        self.image_index = -1
        # Show workspace window
        self.root.deiconify()
        # Show first image
        self.display_next_image()

    def display_next_image(self, offset: int = 1):
        """
        ## Inputs
        offset: int = 1
            The value offset to the right that we will look for the
            next image. Note that we loop around in a circle. Defaults
            to 1. Here, 'next' confusingly refers to time rather than
            space.
        """
        if self.__no_images():
            self.image = None
            # self.panel = None
            warnings.warn('no images available to iterate through.')
        else:
            self.__calculate_next_image_index(offset)
            image_path = self.image_paths[self.image_index]
            self.image = ImageTk.PhotoImage(Image.open(image_path))
            panel = tk.Label(self.root, image=self.image)
            panel.pack(side="bottom", fill="both", expand="yes")


if __name__ == '__main__':
    root = tk.Tk()
    display = Display(root)
    display.display_workspace()

    root.mainloop()
