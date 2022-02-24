from Labelling.config.constants import TEST_IMG_DIR_PATH

import shutil
import os


label_dir = TEST_IMG_DIR_PATH
new_path = os.path.abspath('Labels')

print(new_path)

for path, dirs, files in os.walk(label_dir):
    for file in files:
        if file.lower().endswith('.json'):
            old_loc = os.path.join(path, file)
            old_folder = (os.path.dirname(old_loc).split('\\')[-1])

            new_dir = os.path.join(new_path, old_folder)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)

            new_loc = os.path.join(new_dir, file)
            shutil.copyfile(old_loc, new_loc)

