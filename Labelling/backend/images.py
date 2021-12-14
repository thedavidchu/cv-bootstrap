import os

from PIL import Image

from Labelling.config.constants import TEST_IMG_PATH, TEST_DIR_PATH, IMG_EXT
from paths import standardize_path


def get_image(img_path: str):
    return Image.open(img_path)


class ImagePaths:
    def __init__(self):
        self._img_paths: list = []
        self._idx = 0

    def __len__(self):
        return len(self._img_paths)

    def __getitem__(self, item):
        return get_image(os.path.join(*self._img_paths[item]))

    def __next__(self):
        img = get_image(os.path.join(*self._img_paths[self._idx]))
        self._idx = (self._idx + 1) % len(self._img_paths)
        return img

    def load_dir(self, top_dir_path: str):
        """ Load a directory of images. """
        top_dir_path = standardize_path(top_dir_path)
        # Walk dir_path and get all .jpg, .png, etc files
        for dir_path, dir_names, file_names in os.walk(top_dir_path):
            for file_name in file_names:
                _, file_ext = os.path.splitext(file_name)
                if file_ext.lower() in IMG_EXT:
                    # Get relative path compared to top-level image directory
                    # We will use this knowledge to make labels in a similar
                    # structure to our images, but in a different top-level
                    # directory
                    rel_dir_path = os.path.relpath(dir_path, top_dir_path)
                    self._img_paths.append((top_dir_path, rel_dir_path, file_name))

    def load_file(self, file_path: str):
        file_path = standardize_path(file_path)
        _, file_ext = os.path.splitext(file_path)
        if file_ext.lower() in IMG_EXT:
            dir_path, file_name = os.path.split(file_path)
            self._img_paths.append((dir_path, "", file_name))
        else:
            raise FileNotFoundError("could not find a valid image file")


if __name__ == "__main__":
    test_img_path = TEST_IMG_PATH
    img = get_image(test_img_path)
    img.show()

    x = ImagePaths()
    x.load_dir(TEST_DIR_PATH)
    for img in x:
        img.show()

    y = ImagePaths()
    y.load_file(TEST_IMG_PATH)
    for img in y:
        img.show()
