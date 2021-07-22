import tkinter as tk
import tkinter.filedialog  # Necessary
from PIL import Image, ImageTk
from Preprocessing.server.path import get_paths, filter_image_paths, filter_label_paths
from Preprocessing.server.label import ImageLabels
from Preprocessing.server.modes import CursorMode, GeometryMode
import warnings

SASSY_WARNING = lambda: warnings.warn('lol this does not do anything!')


class Display:

    def __init__(self, root):
        self.root = root
        self.root.title('Label Images')

        self.top_menubar = None
        self.image_frame = tk.LabelFrame(self.root)
        self.tag_frame = tk.LabelFrame(self.root)
        self.bottom_frame = tk.LabelFrame(self.root)

        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)
        self.image_frame.pack(anchor=tk.NW)
        self.bottom_frame.pack(anchor=tk.SW, side=tk.BOTTOM, fill=tk.X)

        self.cursor_mode = CursorMode.NONE
        self.geometry_mode = GeometryMode.NONE

        # image_index = -1 => start at beginning
        self.image_paths = []
        self.label_paths = []
        self.image_index = -1

        self.image_label = ImageLabels
        self.image = None
        self.panel = None

    def __no_images(self):
        """ The selected directory has no valid images. """
        return len(self.image_paths) == 0

    def __next_image_index(self, offset: int = 1):
        """ Get next image index, looping around at the ends. """
        self.image_index = (self.image_index + offset) % len(self.image_paths)

    def _top_menubar(self):
        # Add menu
        self.top_menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(self.top_menubar, tearoff=0)
        file_menu.add_command(label='New', command=SASSY_WARNING)
        file_menu.add_command(label='Open image directory', command=self._open_image_dir)
        file_menu.add_command(label='Open image file', command=self.open_image_file)
        file_menu.add_command(label='Open label directory', command=self._open_label_dir)
        file_menu.add_command(label='Open label file', command=self._open_label_file)
        file_menu.add_separator()
        file_menu.add_command(label='Save Labels', command=SASSY_WARNING)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.root.destroy)
        self.top_menubar.add_cascade(label='File', menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self.top_menubar, tearoff=0)
        edit_menu.add_command(label='Cursor', command=SASSY_WARNING)
        edit_menu.add_command(label='Add point', command=SASSY_WARNING)
        edit_menu.add_command(label='Add line', command=SASSY_WARNING)
        edit_menu.add_command(label='Add polygon', command=SASSY_WARNING)
        edit_menu.add_command(label='Add custom', command=SASSY_WARNING)
        edit_menu.add_command(label='Add full', command=SASSY_WARNING)
        edit_menu.add_command(label='Add tag', command=SASSY_WARNING)
        self.top_menubar.add_cascade(label='Edit', menu=edit_menu)

        # View menu
        view_menu = tk.Menu(self.top_menubar, tearoff=0)
        view_menu.add_command(label='Zoom in', command=SASSY_WARNING)
        view_menu.add_command(label='Zoom out', command=SASSY_WARNING)
        view_menu.add_command(label='A', command=SASSY_WARNING)
        view_menu.add_command(label='B', command=SASSY_WARNING)
        view_menu.add_command(label='C', command=SASSY_WARNING)
        self.top_menubar.add_cascade(label='View', menu=view_menu)

        # Help menu
        help_menu = tk.Menu(self.top_menubar, tearoff=0)
        help_menu.add_command(label='Help...', command=SASSY_WARNING)
        self.top_menubar.add_cascade(label='Help', menu=help_menu)

        self.root.config(menu=self.top_menubar)

    def __create_radio_buttons(self, label, options, row, var=None):
        label_frame = self.bottom_frame
        var = tk.IntVar() if var is None else var
        tk.Label(
            label_frame,
            text=label,
        ).grid(row=row, column=0)
        for i, (option, command) in enumerate(options):
            tk.Radiobutton(
                label_frame,
                variable=var,
                text=option,
                value=i,
                command=command,
                indicatoron=0,
            ).grid(row=row, column=i+1)

    def _cursor_menubar(self):
        def _set_cursor_mode(cursor_mode: CursorMode):
            self.cursor_mode = cursor_mode

        var = tk.IntVar()
        options = [
            ('Select', lambda: _set_cursor_mode(CursorMode.SELECT)),
            ('Click', lambda: _set_cursor_mode(CursorMode.CLICK)),
            ('Drag', lambda: _set_cursor_mode(CursorMode.DRAG)),
        ]
        self.__create_radio_buttons('Cursor', options, 0, var)

    def _geometry_menubar(self):
        def _set_geometry_mode(geometry_mode: GeometryMode):
            self.geometry_mode = geometry_mode

        var = tk.IntVar()
        options = [
            ('None', lambda: _set_geometry_mode(GeometryMode.NONE)),
            ('Point', lambda: _set_geometry_mode(GeometryMode.POINT)),
            ('Line', lambda: _set_geometry_mode(GeometryMode.LINE)),
            ('Polygon', lambda: _set_geometry_mode(GeometryMode.POLYGON)),
            ('Full', lambda: _set_geometry_mode(GeometryMode.FULL)),
            ('Custom', lambda: _set_geometry_mode(GeometryMode.CUSTOM)),
        ]
        self.__create_radio_buttons('Geometry', options, 1, var)

    def _transform_menubar(self):
        pass

    def _tag_menubar(self):
        frame_label = self.tag_frame
        tk.Label(frame_label, text='Tags/Categories').grid(row=0)
        tk.Entry(frame_label).grid(row=1)


    def display_workspace(self):
        # Do on __init__?
        self.root.geometry('500x500')
        self._top_menubar()

        # Bottom menubar
        self._cursor_menubar()
        self._geometry_menubar()
        self._transform_menubar()

        # Right tag bar
        self._tag_menubar()

    # ==================== OPENING DIR AND FILES ==================== #
    def _open_dir(self, filter_fnc):
        # Hide workspace window
        self.root.withdraw()
        # Open '//images' directory by default
        dir_path = tk.filedialog.askdirectory(initialdir='../../')
        print(filter_fnc, dir_path)
        try:
            if filter_fnc == filter_image_paths:
                self.image_paths = get_paths(dir_path, filter_image_paths)
            elif filter_fnc == filter_label_paths:
                self.label_paths = get_paths((dir_path, filter_label_paths))
            else:
                raise ValueError('invalid filter function!')
        except:
            warnings.warn('invalid directory chosen')
        # Show workspace window
        self.root.deiconify()
        # Reset image index
        self.image_index = -1
        # Show first image
        self.display_next_image()

    def _open_file(self, filter_fnc):
        # Hide workspace window
        self.root.withdraw()
        # Open '//images' directory by default
        paths = tk.filedialog.askopenfilenames(initialdir='../../')
        if filter_fnc == filter_image_paths:
            self.image_paths = filter_image_paths(paths)
        elif filter_fnc == filter_label_paths:
            self.label_paths = filter_label_paths(paths)
        else:
            raise ValueError('invalid filter function!')
        # Show workspace window
        self.root.deiconify()
        # Reset image index
        self.image_index = -1
        # Show first image
        self.display_next_image()

    def _open_image_dir(self):
        self._open_dir(filter_image_paths)

    def open_image_file(self):
        self._open_file(filter_image_paths)

    def _open_label_dir(self):
        self._open_dir(filter_label_paths)

    def _open_label_file(self):
        self._open_file(filter_label_paths)

    # ==================== IMAGE DISPLAY ==================== #
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
            self.__next_image_index(offset)
            image_path = self.image_paths[self.image_index]
            self.image = ImageTk.PhotoImage(Image.open(image_path))
            panel = tk.Label(self.image_frame, image=self.image)
            panel.grid(row=0, column=0)


if __name__ == '__main__':
    pass
    root = tk.Tk()
    display = Display(root)
    display.display_workspace()
    root.mainloop()

    # from tkinter import *
    # top = Tk()
    # Lb1 = Listbox(top)
    # Lb1.insert(1, "Python")
    # Lb1.insert(2, "Perl")
    # Lb1.insert(3, "C")
    # Lb1.insert(4, "PHP")
    # Lb1.insert(5, "JSP")
    # Lb1.insert(6, "Ruby")
    #
    # Lb1.pack()
    # top.mainloop()

