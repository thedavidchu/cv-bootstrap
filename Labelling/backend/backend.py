""" Main file that will store the states. """

from images import ImagePaths

class Backend:
    def __init__(self):
        self.images = ImagePaths()
        self.labels = {}
        self.label_dir_path = ""
