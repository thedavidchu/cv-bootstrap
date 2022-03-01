import os
import shutil
from Labelling.backend.paths import standardize_path


def move_files(
    src_dir: str,
    dst_dir: str,
    file_ext: set,
):
    """Given a source and destination path, copy the files with a given file
    extension.

    ## Notes
    1. See shutil.copytree(src, dst, ignore=shutil.include_patterns("*.json")), """
    # Normalize paths
    src_dir = standardize_path(src_dir)
    dst_dir = standardize_path(dst_dir)

    # Walk src_dir and move all LABEL_FILE_EXTENSIONS files to dst_dir
    for old_dirpath, dirnames, filenames in os.walk(src_dir):
        # Get difference between source and old directories
        diff_dir = os.path.relpath(standardize_path(old_dirpath), start=src_dir)

        # Keep only .json files (take lowercase of file extension)
        filenames = tuple(filter(
            lambda fn: os.path.splitext(fn)[-1].lower() in file_ext,
            filenames
        ))

        new_dirpath = os.path.join(dst_dir, diff_dir)
        if filenames and not os.path.exists(new_dirpath):
            os.mkdir(new_dirpath)

        # Copy files from src -> dst
        for fn in filenames:
            old_full_path = os.path.join(old_dirpath, fn)
            new_full_path = os.path.join(new_dirpath, fn)
            shutil.copyfile(old_full_path, new_full_path)
