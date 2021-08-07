"""
TODO
1. Clean up the code obviously.
2. Move stuff to other functions/ classes. Namely, images and labels.
"""


import tkinter as tk
import tkinter.filedialog  # Necessary
import json
import warnings
from PIL import Image, ImageTk
from Preprocessing.server.path import get_paths, filter_image_paths, filter_label_paths
from Preprocessing.server.label import ImageLabels
from Preprocessing.server.modes import CursorMode, GeometryMode
from shapely import geometry as g

SASSY_WARNING = lambda: warnings.warn('lol this does not do anything!')
_TESTING_MODE = True

def save_as_json(to_save: dict):
    # Convert wkt to well-known text
    for abs_image_path, labels in to_save.items():
        for label in labels:
            if isinstance(label['wkt'], str):
                continue
            label['wkt'] = label['wkt'].wkt
    with open('../../labels/labels.json', 'w') as f:
        json.dump(to_save, f, indent=4)

class Display:
    def __init__(self, root):
        self.root = root
        self.root.title('Label Images')
        self.canvas = None

        # Menu bar
        self.top_menubar = None
        # Top frame
        self.top_frame = tk.LabelFrame(self.root)
        self.image_frame = tk.LabelFrame(self.top_frame)
        self.tag_frame = tk.LabelFrame(self.top_frame)
        # Bottom frame
        self.bottom_frame = tk.LabelFrame(self.root)
        # Pack frames
        self.bottom_frame.pack(anchor=tk.SW, side=tk.BOTTOM, fill=tk.X)
        self.top_frame.pack(anchor=tk.N, fill='both')
        self.tag_frame.pack(anchor=tk.NE, side=tk.RIGHT)
        self.tag = None
        self.image_frame.pack(anchor=tk.NW)

        # Modes
        self.cursor_mode = CursorMode.NONE
        self.geometry_mode = GeometryMode.NONE

        # Image
        # image_index = -1 => start at beginning
        self.image_paths = []
        self.label_paths = []
        self.image_index = -1

        # Labels
        self.image_label = ImageLabels
        self.image = None
        self.panel = None
        self.raw_points = []

        self.tk_marks = []
        self.processed_geometry = {}

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
            ).grid(row=row, column=i + 1)

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
        self.tag = tk.Entry(frame_label)
        self.tag.grid(row=1)

    def display_workspace(self):
        # Do on __init__?
        self.root.geometry('500x500')
        self._top_menubar()

        # Bottom menubar
        self._cursor_menubar()
        self._geometry_menubar()
        self._transform_menubar()  # Note implemented

        # Right tag bar
        self._tag_menubar()

        # TESTING MODE
        if _TESTING_MODE:
            self.image_paths = get_paths('../../images/', filter_image_paths)
            self.image_index = -1
            self.display_next_image()

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
        except NotADirectoryError:
            warnings.warn('invalid directory chosen')
        except ValueError:
            warnings.warn('invalid filter function!')
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
            warnings.warn('no images available to iterate through.')
        else:
            self.__next_image_index(offset)
            image_path = self.image_paths[self.image_index]
            ## TO DELETE
            self.canvas = tk.Canvas(master=self.top_frame, width=500, height=500)
            self.canvas.pack(side=tk.LEFT, anchor=tk.NW)
            self.canvas.bind("<B1-Motion>", self.draw_point_and_line)
            self.root.bind("<BackSpace>", self.delete_point)
            self.root.bind("<Return>", self.save_points)
            ## END TO DELETE
            self.image = ImageTk.PhotoImage(Image.open(image_path))
            self.canvas.create_image(200, 200, anchor=tk.NW, image=self.image)

    def draw_point_and_line(self, event):
        # From https://www.python-course.eu/tkinter_canvas.php
        python_green = "#476042"
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)

        if self.raw_points:
            line = self.canvas.create_line(event.x, event.y, self.raw_points[-1].x, self.raw_points[-1].y)
            self.tk_marks.append(line)
        oval = self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)
        self.tk_marks.append(oval)

        self.raw_points.append(g.Point(event.x, event.y))

    def delete_point(self, event):
        if self.tk_marks:
            oval = self.tk_marks.pop()
            self.canvas.delete(oval)
        else:
            warnings.warn('No more points!')
        if self.tk_marks:
            line = self.tk_marks.pop()
            self.canvas.delete(line)
        else:
            warnings.warn('last point!')

    def save_points(self, event):
        abs_image_path = self.image_paths[self.image_index]
        if abs_image_path in self.processed_geometry:
            pass
        else:
            self.processed_geometry[abs_image_path] = []
        tag = self.tag.get()
        if self.geometry_mode == GeometryMode.NONE:
            warnings.warn('no mode selected')
            return
        elif self.geometry_mode == GeometryMode.POINT:
            warnings.warn('not implemented')
            return
        elif self.geometry_mode == GeometryMode.LINE:
            point_processor = g.LineString
        elif self.geometry_mode == GeometryMode.POLYGON:
            point_processor = g.Polygon
        else:
            warnings.warn('not implemented')
            return

        self.processed_geometry[abs_image_path].append(
            {
                'tag': tag,
                "order": len(self.processed_geometry[abs_image_path]),
                "wkt": point_processor(self.raw_points)
            }
        )

        for i in range(len(self.tk_marks)):
            self.canvas.delete(self.tk_marks.pop())

        print(self.processed_geometry)
        save_as_json(self.processed_geometry)


if __name__ == '__main__':
    root = tk.Tk()
    display = Display(root)
    display.display_workspace()
    root.mainloop()
