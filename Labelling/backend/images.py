import os
from typing import List, Tuple

from PIL import Image

from Labelling.backend.paths import standardize_path
from Labelling.constants.constants import IMAGE_FILE_EXTENSIONS
from Labelling.graphics.popup.popup import show_error, show_warning


def get_image(img_path: str):
    return Image.open(img_path)


class ImagePaths:
    """ An over-engineered, glorified list of image paths that loads paths lazily."""

    def __init__(self):
        self._img_paths: List[Tuple[str, str, str]] = []
        self._idx = 0

    def __len__(self):
        return len(self._img_paths)

    def __getitem__(self, item):
        return get_image(os.path.join(*self._img_paths[item]))

    def __repr__(self):
        return repr(tuple(map(lambda x: os.path.join(*x), self._img_paths)))

    # Error handling
    def assert_contains_image(self):
        if not len(self._img_paths):
            show_error("No images", "No images are selected for labelling")
            raise ValueError("No images")

    # Get paths
    def get_idx(self):
        return self._idx

    def get_image_path(self):
        return os.path.join(*self._img_paths[self._idx])

    def get_label_path(self) -> str:
        """Return the current label path of the current label."""
        full_path = self.get_image_path()
        pre, ext = os.path.splitext(full_path)
        r = pre + ".json"
        return r

    # Get images
    def get_image(self):
        self.assert_contains_image()
        return get_image(self.get_image_path())

    def next_image(self):
        self.assert_contains_image()
        self._idx = (self._idx + 1) % len(self._img_paths)
        return get_image(self.get_image_path())

    def prev_image(self):
        self.assert_contains_image()
        self._idx = (self._idx - 1) % len(self._img_paths)
        return get_image(self.get_image_path())

    def set_image(self, idx):
        self.assert_contains_image()
        self._idx = idx % len(self._img_paths)

        if idx >= len(self._img_paths):
            show_warning("Index larger than number of images", "Uh-oh. I moduloed it")
        return get_image(self.get_image_path())

    # Load paths
    def load_dir(self, top_dir_path: str):
        """ Load a directory of images. """
        self._idx = 0
        top_dir_path = standardize_path(top_dir_path)
        # Walk dir_path and get all .jpg, .png, etc files
        for dir_path, dir_names, file_names in os.walk(top_dir_path):
            for file_name in file_names:
                _, file_ext = os.path.splitext(file_name)
                if file_ext.lower() in IMAGE_FILE_EXTENSIONS:
                    # Get relative path compared to top-level image directory
                    # We will use this knowledge to make labels in a similar
                    # structure to our images, but in a different top-level
                    # directory
                    rel_dir_path = os.path.relpath(dir_path, top_dir_path)
                    self._img_paths.append((top_dir_path, rel_dir_path, file_name))

    def load_files(self, file_paths: Tuple[str]):
        self._idx = 0
        for file_path in file_paths:
            self.load_file(file_path)

    def load_file(self, file_path: str):
        self._idx = 0
        file_path = standardize_path(file_path)
        _, file_ext = os.path.splitext(file_path)
        if file_ext.lower() in IMAGE_FILE_EXTENSIONS:
            dir_path, file_name = os.path.split(file_path)
            self._img_paths.append((dir_path, "", file_name))
        else:
            raise FileNotFoundError("could not find a valid image file")


if __name__ == "__main__":
    TEST_IMG_FILE_PATH: str = "../../data/images/airplane/1.jpg"
    TEST_IMG_DIR_PATH: str = "../../data/images/"

    test_img_path = TEST_IMG_FILE_PATH
    img = get_image(test_img_path)
    img.show()

    x = ImagePaths()
    x.load_dir(TEST_IMG_DIR_PATH)
    for img in x:
        img.show()

    y = ImagePaths()
    y.load_file(TEST_IMG_FILE_PATH)
    for img in y:
        img.show()
