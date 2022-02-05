from cProfile import label
from lib2to3.pytree import LeafPattern
from Labelling.config.constants import TEST_IMG_DIR_PATH

import shutil
import os


LABEL_DIR = TEST_IMG_DIR_PATH
NEW_PATH = os.path.abspath('Labels')

print(NEW_PATH)

for path, dirs, files in os.walk(LABEL_DIR):
    for file in files:
        if file.endswith('json'):
            OLD_LOC = os.path.join(path, file)
            OLD_FOLDER = (os.path.dirname(OLD_LOC).split('\\')[-1])

            NEW_DIR = os.path.join(NEW_PATH, OLD_FOLDER)
            if not os.path.exists(NEW_DIR):
                os.mkdir(NEW_DIR)

            NEW_LOC = os.path.join(NEW_DIR, file)
            shutil.copyfile(OLD_LOC, NEW_LOC)

