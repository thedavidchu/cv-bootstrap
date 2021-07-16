import argparse
import os
import re


def get_image_paths(dir_path: str):
    image_paths = []
    for dir_or_file in os.scandir(dir_path):
        if os.path.isdir(dir_or_file.path):
            image_paths.extend(get_image_paths(dir_or_file.path))
        elif re.match(r'^.*\.(jpe?g|png)$', dir_or_file.path.lower()):
            image_paths.append(dir_or_file.path)
        else:
            continue

    return image_paths


if __name__ == '__main__':
    image_paths = get_image_paths('images')