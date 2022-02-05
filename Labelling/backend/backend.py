""" Main file that will store the states. """
import json

from Labelling.backend.images import ImagePaths


class Backend:
    def __init__(self, app):
        self.app: type(app) = app
        self.image_paths: ImagePaths = ImagePaths()

        try:
            with open("config.json") as f:
                self.author: str = json.load(f)["author"]
        except (FileNotFoundError, KeyError):
            self.author: str = ""
